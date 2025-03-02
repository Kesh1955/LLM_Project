# **ConvFinQA Prompt Evaluation & Analysis**

This repository contains the evaluation and analysis of **ConvFinQA** dataset responses using different **LLM prompt techniques**. The project is focused on **evaluating numerical answer correctness and program equivalence**, testing few-shot, CoT, and other prompting strategies.

## **🔍 Project Overview**
This project explores:
- How well different **LLM prompt techniques** (e.g., Chain-of-Thought, Few-Shot) perform in **answer extraction** and **program generation**.
- The **accuracy of numerical responses** using **exact match**.
- The **equivalence of generated programs** to gold programs (ground truth).
- Using **LLMs as a judge** to evaluate program correctness.

## **📂 Folder Structure**


- **project/**
  - `data/` - Original dataset (JSON from ConvFinQA repo)
    - `filtered_data/` - Processed dataset (filtered JSON)
    - `answer_data/` - CSV outputs from different answer-based prompt techniques
    - `program_data/` - CSV outputs from different program-based prompt techniques
  - `Evaluate_metrics/` - Summarizing results
    - `Answer.ipynb` - Analysis & findings for answer-based prompts
    - `Program.ipynb` - Analysis & findings for program-based prompts
  - `project/`
    - `01_Answer_Eval.ipynb` - Main notebook for loading & testing answers
    - `02_Program_Eval.ipynb` - Main notebook for loading & testing programs
  - `src/` - Source code & system prompts
    - `answer_prompt/` - Prompts used for extracting answers
    - `program_prompt/` - Prompts used for generating programs
    - `LLM_as_judge/` - Prompts for evaluating program equivalence with LLMs
  - `README.md` - This file
  - `.gitignore` - Files & folders to ignore in Git


 ## **📊 Dataset**
We use **ConvFinQA**, a financial reasoning dataset that extends **FinQA** by incorporating multi-turn question-answering with numerical reasoning.

- 📜 Paper: [ACL Anthology](https://arxiv.org/abs/2210.03849)
- 📂 Dataset Source: [ConvFinQA GitHub](https://github.com/czyssrs/ConvFinQA)


## **Running Evaluation**
Answer-Based Evaluation:
Open 01_Answer_Eval.ipynb to explore, test, and evaluate numerical answer correctness.

 ## **Program-Based Evaluation**
Open 02_Program_Eval.ipynb to test the model’s ability to generate mathematically equivalent programs.

 ## **Understanding Results**
Use Evaluate_metrics/Answer.ipynb for summary findings on answer accuracy.
Use Evaluate_metrics/Program.ipynb for insights on program correctness.

## **🚀 How to Use**

### **Setup**
```bash
git clone https://github.com/Kesh1955/LLM_Project.git
cd project

Install poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

Install dependencies
poetry install # This will install all dependencies listed in pyproject.toml 
               # and ensure a consistent environment using the poetry.lock file.

Activate Virtual Env manage by Poetry
poetry shell

Alternative: Using pip Instead of Poetry
If you prefer pip over Poetry, you can export the dependencies and install them manually
poetry export -f requirements.txt --output requirements.txt
pip install -r requirements.txt
```

