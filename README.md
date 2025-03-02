# **ConvFinQA Prompt Evaluation & Analysis**

This repository contains the evaluation and analysis of **ConvFinQA** dataset responses using different **LLM prompt techniques**. The project is focused on **evaluating numerical answer correctness and program equivalence**, testing few-shot, CoT, and other prompting strategies.

## **🔍 Project Overview**
This project explores:
- How well different **LLM prompt techniques** (e.g., Chain-of-Thought, Few-Shot) perform in **answer extraction** and **program generation**.
- The **accuracy of numerical responses** using **exact match**.
- The **equivalence of generated programs** to gold programs (ground truth).
- Using **LLMs as a judge** to evaluate program correctness.

## **📂 Folder Structure**

project/ │── data/ # Original dataset (JSON from ConvFinQA repo) │── filtered_data/ # Processed dataset (filtered JSON) │── answer_data/ # CSV outputs from different answer-based prompt techniques │── program_data/ # CSV outputs from different program-based prompt techniques │── Evaluate_metrics/ # Summarizing results │ ├── Answer.ipynb # Analysis & findings for answer-based prompts │ ├── Program.ipynb # Analysis & findings for program-based prompts │── 01_Answer_Eval.ipynb # Main notebook for loading & testing answers │── 02_Program_Eval.ipynb # Main notebook for loading & testing programs │── src/ # Source code & system prompts │ ├── answer_prompt/ # Prompts used for extracting answers │ ├── program_prompt/ # Prompts used for generating programs │ ├── LLM_as_judge/ # Prompts for evaluating program equivalence with LLMs │── README.md # This file │── .gitignore # Files & folders to ignore in Git

<!-- 'Evaluation_metrics' - has 2 notebooks:
    (i) Answer.ipynb - Calling in csvs from 'answer_data' to more neatly summarise findings and limitations
    (ii) Program.ipynb - Calling in csvs from 'program_data' to more neatly summarise findings and limitations

'01_Answer_Eval.ipynb' & '02_Program_Eval.ipynb' - Most of the work to load, explore, test and eval data is in here. More detailed information at each step in the process.

'data' - Original json data from ConvFinQA Github: https://github.com/czyssrs/ConvFinQA. Paper is here: https://arxiv.org/abs/2210.03849
'filtered_data' -  is the new json created once I've filtered out unecessary keys 
'program_data' - is the csv outputs from analyses and different prompt techniques
'answer_data' - is the csv outputs from analyses and different prompt techniques

'src'
'answer_prompt' - System prompts from 'answer'
'program_prompt - System prompts from 'program'
'LLM_as_judge' - System prompts from using LLM as a judge -->




 ## **📊 Dataset**
We use **ConvFinQA**, a financial reasoning dataset that extends **FinQA** by incorporating multi-turn question-answering with numerical reasoning.

- 📜 Paper: [ACL Anthology](https://arxiv.org/abs/2210.03849)
- 📂 Dataset Source: [ConvFinQA GitHub](https://github.com/czyssrs/ConvFinQA)

## **🚀 How to Use**
### **1️⃣ Setup**
```bash
git clone https://github.com/your-repo-name.git ### To-do 
cd project
pip install -r requirements.txt  # (if dependencies are needed) ### to-do 


2️⃣ Running Evaluation
Answer-Based Evaluation:
Open 01_Answer_Eval.ipynb to explore, test, and evaluate numerical answer correctness.

Program-Based Evaluation:
Open 02_Program_Eval.ipynb to test the model’s ability to generate mathematically equivalent programs.
3️⃣ Understanding Results
Use Evaluate_metrics/Answer.ipynb for summary findings on answer accuracy.
Use Evaluate_metrics/Program.ipynb for insights on program correctness.
