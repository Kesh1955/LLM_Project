# **ConvFinQA Prompt Evaluation & Analysis**

This repository contains the evaluation and analysis of **ConvFinQA** dataset responses using different **LLM prompt techniques**. The project is focused on **evaluating numerical answer accuracy and program equivalence**, testing few-shot, CoT, and other prompting strategies.

## **🔍 Project Overview**
This project explores:
- How well different **LLM prompt techniques** (e.g., Basic prompts, Few-Shot) perform in **answer extraction** and **program generation**.
- Using **LLMs as a judge** to evaluate program correctness.


**Eval Metrics**
- 1. The **accuracy of numerical responses** using **exact match: fail(0) or pass(1)**.
- 2. The **accuracy of numerical responses** using **exact match (between 0 or 1, where 0 means completely different and 1 means virtually identical)**.
- 3. The **equivalence of generated programs** to gold programs (ground truth).


## **📂 Folder Structure**

- **project/**
  - `data/` - Original dataset (JSON from ConvFinQA repo)
    - `answer_data/` - CSV outputs from different answer-based prompt techniques
    - `program_data/` - CSV outputs from different program-based prompt techniques
  - `Evaluate_metrics_summary_notebooks/` - Summarizing results
    - `Answer.ipynb` - Analysis & findings for answer-based prompts
    - `Program.ipynb` - Analysis & findings for program-based prompts
    - `Answer_and_Prog_Eval.ipynb` - Lesson learned from 01 and 02 I implemented in here:
                                         (i) Pydantic structured outputs
                                         (ii) less pre-processing answer
                                         (iii) Answer eval exatch match between 0-1
                                        (iv) Program Equivalence is the same 0/1
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
Open 01_Answer_Eval.ipynb to explore, test, and evaluate numerical answer accuracy.

 ## **Program-Based Evaluation**
Open 02_Program_Eval.ipynb to test the model’s ability to generate mathematically equivalent programs.

 ## **Answer & Program Evaluation** 
This approach took lessons learns from the 2 above (adding in Pydantic structured outputs, improved prompt engineering)
Additionally the way in which answer accuracy is evaluated is between 0-1
Open Evaluate_metrics_summary_notebooks/Answer_and_Prog_Eval.ipynb to explore, test, and evaluate numerical answer accuracy and test the model’s ability to generate mathematically equivalent programs.


 ## **Understanding Results**
Use Evaluate_metrics_summary_notebooks/Answer.ipynb for summary findings on answer accuracy.
Use Evaluate_metrics_summary_notebooks/Program.ipynb for insights on program correctness.
Use Evaluate_metrics_summary_notebooks/Answer_and_Prog_Eval.ipynb for insights on findings and lessons learned from previous runs

## **🚀 How to Use**

### **Setup**
```bash
git clone https://github.com/Kesh1955/LLM_Project.git
cd project

Install poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

Install dependencies
poetry install 

Activate Virtual Env manage by Poetry
poetry shell

Alternative: Using pip Instead of Poetry
If you prefer pip over Poetry, you can export the dependencies and install them manually
poetry export -f requirements.txt --output requirements.txt
pip install -r requirements.txt
```

