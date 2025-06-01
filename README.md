# From Thinking to Output: Chain-of-Thought and Text Generation Characteristics in Reasoning Language Models

This is the official repository for the paper:

"**From Thinking to Output: Chain-of-Thought and Text Generation Characteristics in Reasoning Language Models**".

**Authors**: Junhao Liu, Zhenhao Xu, Yuxin Fang, Yichuan Chen and Wenhan Chang*

---

### Abstract

Recently, there have been notable advancements in large language models (LLMs), demonstrating their growing abilities in complex reasoning. However, existing research largely overlooks a thorough and systematic comparison of these models' reasoning processes and outputs, particularly regarding their self-reflection pattern (also termed "Aha moment") and the interconnections across diverse domains. This paper proposes a novel framework for analyzing the reasoning characteristics of four cutting-edge large reasoning models (GPT-o1, DeepSeek-R1, Kimi-k1.5, and Grok-3) using keywords statistic and LLM-as-a-judge paradigm. Our approach connects their internal thinking processes with their final outputs. A diverse dataset consists of real-world scenario-based questions covering logical deduction, causal inference, and multi-step problem-solving. Additionally, a set of metrics is put forward to assess both the coherence of reasoning and the accuracy of the outputs. The research results uncover various patterns of how these models balance exploration and exploitation, deal with problems, and reach conclusions during the reasoning process. Through quantitative and qualitative comparisons, disparities among these models are identified in aspects such as the depth of reasoning, the reliance on intermediate steps, and the degree of similarity between their thinking processes and output patterns and those of GPT-o1. This work offers valuable insights into the trade-off between computational efficiency and reasoning robustness and provides practical recommendations for enhancing model design and evaluation in practical applications.

---

### Repository Contents

In this repository, you'll find the core data and results from our research. We've initially provided:

* **Raw data** used in the paper's experiments.
* The **LLM reasoning processes and outputs** obtained through API calls.
* Results from the paper's evaluation, including **keyword statistics** and **LLM-as-a-judge scores**.

---

### Future Plans

We're currently organizing our code and will be submitting it to this repository soon. For the specific prompts used in the LLM-as-a-judge evaluations, please refer to the **appendix of our paper**.
