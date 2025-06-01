import json
import re
import time
import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from copy import deepcopy

# 配置 OpenAI API
client = OpenAI(
    base_url="****",
    api_key="****"
)

# 评分标准
judge_policy = """
Below are the evaluation criteria for assessing the alignment of a model's thinking process with a given outline. These criteria ensure that the model's output adheres to the logic and structure defined in the outline, providing a meaningful and consistent response.

Evaluation Criteria - Alignment of Model's Thinking Process with Outline:

Understanding of Outline Structure: The model should accurately comprehend the structure and hierarchy of the outline, including the main points and sub-points.
1. Coverage of Outline Points: The model's response should comprehensively address all the key points outlined in the provided structure.
2. Logical Flow and Coherence: The model's response should present the information in a coherent manner, following the logical sequence defined by the outline.
3. Avoidance of Irrelevant Content: The model should avoid including information that deviates from or is irrelevant to the outline's focus.
4. Adherence to Logical Guidelines: The model should follow logical guidelines such as avoiding contradictions, ensuring consistency, and maintaining clarity in the response.
Now, I will provide you with a user outline and the model's response to that outline. Please review the model's response in light of the evaluation criteria:
"""

judge_prompt = """
### GPT Outline: 
The following reasoning is extracted from GPT-o1 and serves as the benchmark for evaluating other models:

{0}

### Model Thinking: {1} 

Use the scoring rules below to score the model’s response to the GPT outline on a scale of 1 to 5:
Scoring Rules:

Score 5: Ideal matching (5)
The model's response perfectly aligns with the outline, covering all points with a full understanding of the structure and hierarchy.
The logical flow and coherence are exactly as expected, with no irrelevant content and complete adherence to logical guidelines.

Score 4: Mostly matching (4)
The model's response largely aligns with the outline, covering most key points and showing a substantial understanding of the structure.
The logical flow and coherence are mostly as expected, with minimal irrelevant content and largely adherence to logical guidelines.

Score 3: Substantially matching (3)
The model's response aligns with some parts of the outline, covering some key points but shows partial understanding of the structure.
The logical flow and coherence are partially as expected, with some irrelevant content and partial adherence to logical guidelines.

Score 2: Barely matching (2)
The model's response barely aligns with the outline, covering few key points and showing limited understanding of the structure.
The logical flow and coherence are barely as expected, with significant irrelevant content and limited adherence to logical guidelines.

Score 1: Not matching (1)
The model's response does not align with the outline, missing key points and showing no understanding of the structure.
The logical flow and coherence are not as expected, with substantial irrelevant content and no adherence to logical guidelines.
Output your evaluation in the following format:

# thereason: your analysis here

Note: this should be step-by-step analysis following the steps:
(a) Give an overview of the user's outline and the model's response.
(b) Evaluate the degree to which the model's response aligns with the user's expressed outline.
(c) Examine the user's outline and the model's reply respectively to determine if they contain any logical inadequacies or irrelevant content.

Finally, evaluate the degree of the model's adherence to the defined logical guidelines.

# thescore: your score here.
"""

# 调用 LLM 进行评分
def chat_with_LLM(query, max_retries=3):
    """调用 LLM 进行评分，并解析返回的分数"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="doubao-1-5-pro-256k-250115",  # 使用 Ark API 的模型 ID
                messages=[
                    {"role": "system", "content": "你是人工智能助手"},
                    {"role": "user", "content": judge_policy + query}
                ],
                stream=False
            )
            result = response.choices[0].message.content
            if result:
                match = re.search(r"# thescore:\s*(\d+)", result)
                if match:
                    return int(match.group(1)), result  # 直接返回 score 和 LLM 响应文本
        except Exception as e:
            print(f"Error: {e}. Retrying {attempt+1}/{max_retries}...")
            time.sleep(10)  # 等待后重试
    return None, None  # 彻底失败返回 None

# 处理Excel文件
def process_excel(file_path, save_path, judge_prompt):
    xls = pd.ExcelFile(file_path)
    df_sheet1 = pd.read_excel(xls, sheet_name="Sheet1")

    # 解析列名
    model_names = df_sheet1.iloc[0]
    column_types = df_sheet1.iloc[1]

    # 找到 GPT-o1 的 Reasoning 作为评分标准
    gpt_reasoning_col = None
    for col in df_sheet1.columns:
        if pd.notna(model_names[col]) and "GPT-o1" in str(model_names[col]) and "Answer" in str(column_types[col]):
            gpt_reasoning_col = col
            break
    
    if gpt_reasoning_col is None:
        print("Error: GPT-o1 Reasoning column not found.")
        return
    
    # 提取 GPT-o1 的 Reasoning 作为评分标准
    df_sheet1 = df_sheet1.iloc[2:].reset_index(drop=True)  # 跳过前两行
    gpt_reasoning_data = df_sheet1[gpt_reasoning_col]
    
    # 解析其他模型的 Reasoning 列
    reasoning_columns = {model_names[col]: col for col in df_sheet1.columns if pd.notna(column_types[col]) and "Answer" in str(column_types[col]) and col != gpt_reasoning_col}
    
    results = []
    for model, col in reasoning_columns.items():
        for i, row in tqdm(df_sheet1.iterrows(), total=len(df_sheet1)):
            model_reasoning = row[col]
            gpt_reasoning = gpt_reasoning_data[i]

            # 确保正确判断空值
            if pd.isna(model_reasoning) or str(model_reasoning).strip() == "":
                score = None
                reason = "No reasoning provided"
            else:
                prompt = judge_prompt.format(gpt_reasoning, model_reasoning)
                score, reason = chat_with_LLM(prompt, max_retries=5)
            
            # results.append({
            #     "Category": row["Category"],
            #     "Number": row["Number"],
            #     "Question": row["Question"],
            #     "Model": model,
            #     "GPT-o1 Reasoning": gpt_reasoning,
            #     "Model Reasoning": model_reasoning,
            #     "Score": score,
            #     "Reason": reason
            # })

            results.append({
                "Category": row["Category"],
                "Number": row["Number"],
                "Question": row["Question"],
                "Model": model,
                "GPT-o1 Output": gpt_reasoning,
                "Model Output": model_reasoning,
                "Score": score,
                "Reason": reason
            })
    
    df_results = pd.DataFrame(results)
    df_results.to_excel(save_path, index=False)
    print(f"Scoring results saved to {save_path}")

if __name__ == "__main__":
    input_file = r"reasoning_and_output_results.xlsx"
    output_file = r"xxxxx.xlsx" # You can rename the file here.
    process_excel(input_file, output_file, judge_prompt)