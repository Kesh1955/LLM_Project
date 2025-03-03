import json 
import pandas as pd
import string 
import re 
import openai


# Convert the table data into html
def to_html(table_data: pd.DataFrame) -> str:
    """
    Converts a list-of-lists into an HTML table.
    The first row is treated as column headers (<th>).
    Subsequent rows become table body (<tbody>) rows (<tr><td>...</td></tr>).

    :param table_data: A 2D list representing rows of the table.
                      e.g. [
                          ["", "as of december 31 2014 (in percentages)"],
                          ["infraserv gmbh & co . gendorf kg", "39"],
                          ["infraserv gmbh & co . hoechst kg", "32"]
                      ]
    :return: A string of HTML markup for the table.
    """

    # Handle empty or invalid input
    if not table_data or not isinstance(table_data, list) or len(table_data) == 0:
        return "<table></table>"

    # Start building the HTML string
    html_string = "<table>\n  <thead>\n    <tr>\n"

    # Use the first row as headers
    headers = table_data[0]
    for th in headers:
        html_string += f"      <th>{th}</th>\n"
    html_string += "    </tr>\n  </thead>\n"

    # Add the table body
    html_string += "  <tbody>\n"
    for row in table_data[1:]:
        html_string += "    <tr>"
        for td in row:
            html_string += f"<td>{td}</td>"
        html_string += "</tr>\n"
    html_string += "  </tbody>\n</table>"

    return html_string



# Allows to inspect data based on index to understand details of output
# For example some examples might be missing answers etc...
def inspect_item(df: pd.DataFrame, index) -> str:
    """
    Display all key-value pairs for a specific item in a readable format.
    Uses JSON formatting for clean, indented output of nested structures.
    """
    print(f"\nInspecting item at index {index}:")
    print("-" * 50)

    # Get the item and format it nicely using JSON
    item = df[index]
    formatted_item = json.dumps(item, indent=2)
    print(formatted_item)

    # Also show a simple list of top-level keys for quick reference
    print("\nTop-level keys in this item:")
    print(list(item.keys()))





def robust_extract_float(s: str):
    """
    Attempts to extract the *final* float from the input string 's', handling:
      - Commas (e.g., "17,019.5" -> "17019.5")
      - Optional minus sign (with potential whitespace).
      - Optional currency symbols ($, £, €).
      - Optional trailing letters K, M, B (removed but NOT interpreted).
      - Optional trailing '%'.

    Returns:
        float: The extracted float value, if found.
        None : If no valid numeric portion is found.
    """
    # 1) Remove commas (e.g., "17,019.5" -> "17019.5")
    s = s.replace(",", "")

    # Regex Explanation:
    #   -?              optional minus sign
    #   \s*             optional whitespace
    #   [£$\€]?         optional currency symbol
    #   \s*             optional whitespace
    #   \d+             one or more digits
    #   (?:\.\d+)?      optional decimal + digits
    #   \s*             optional whitespace
    #   [KkMmBb]?       optional K, M, or B suffix
    #   \s*%?           optional whitespace + optional '%'

    pattern = r"-?\s*[£$\€]?\s*\d+(?:\.\d+)?\s*[KkMmBb]?\s*%?"

    # 2) Find all matches and take the last one if any exist
    matches = re.findall(pattern, s)
    if not matches:
        return None

    # The 'final' numeric substring is the last match
    val = matches[-1]

    # Remove any remaining spaces
    val = val.replace(" ", "")

    # Remove currency symbols
    for symbol in ["$", "€", "£"]:
        val = val.replace(symbol, "")

    # Remove trailing % sign
    val = val.strip("%")

    # Remove trailing K, M, B letters (no numeric interpretation)
    for suffix in ["K", "k", "M", "m", "B", "b"]:
        if val.endswith(suffix):
            val = val[:-1]
            break

    # Convert to float
    try:
        return float(val)
    except ValueError:
        return None


# Normalise answer
import re

def normalize_answer(s: str) -> float:
    s = s.strip()
    s_no_commas = s.replace(",", "")
    pattern = r"-?\s*[£$\€]?\s*\d+(?:\.\d+)?\s*[KkMmBb]?\s*%?"
    matches = re.findall(pattern, s_no_commas)
    if not matches:
        return None
    
    val_str = matches[-1]
    val_str = val_str.replace(" ", "")
    
    # Remove currency symbols
    for sym in ["$", "€", "£"]:
        val_str = val_str.replace(sym, "")
    
    # If a trailing '%' exists, just remove it (no longer divide by 100)
    if val_str.endswith('%'):
        val_str = val_str[:-1]
    
    # Remove trailing K, M, B
    if val_str.endswith(('K', 'k', 'M', 'm', 'B', 'b')):
        val_str = val_str[:-1]
    
    # Attempt float conversion
    try:
        numeric_val = float(val_str)
    except ValueError:
        return None
    
    return numeric_val







#######

def process_records(records, system_prompts, model_name,prompt_style, table_key, model_pred_col_name):
    """
    For each record, calls OpenAI and returns a DataFrame with columns:
      [id, question, gold_answer, program, table, html_table,
       <answer_col_name>, model, prompt_style, prompt]

    'model_pred_col_name' is the column under which the model's answer is stored.
    By default, it's 'model_answer', but you can override it (e.g. 'program_prediction').
    """
    results = []
    for r in records:
        # Build messages (unchanged)
        messages = construct_main_messages(r, system_prompts, table_key=table_key)
        try:
            response = openai.chat.completions.create(
                model=model_name,
                messages=messages
            )
            llm_answer = response.choices[0].message.content.strip()
        except Exception as e:
            llm_answer = f"Error: {e}"

        # Build the results row
        row_dict = {
            "id": r["id"],
            "question": r["question"],
            "gold_answer": r.get("gold_answer", ""),
            "clean_gold_answer": r.get("clean_gold_answer"),
            "program": r.get("program", ""),
            "table": r.get("table", ""),
            "html_table": r.get("html_table", ""),
            "model": model_name,
            "prompt_style": prompt_style,
            "prompt": system_prompts, 
        }
        # Dynamically store the LLM’s answer in whichever column name was specified
        row_dict[model_pred_col_name] = llm_answer

        results.append(row_dict)

    return pd.DataFrame(results)







def construct_main_messages(record: dict, system_prompts: dict, table_key: str) -> list:
    """
    Builds the final messages by looking up a prompt in system_prompts["system_prompt"],
    then formatting placeholders {pre_text}, {post_text}, and {table} with data from record.

    'table_key' lets you choose which column to use (e.g. "table" or "html_table").
    We assume the system prompt references {table}, so we pass table=record.get(table_key,"").
    """
    system_prompt_template = system_prompts["system_prompt"]

    system_message_content = system_prompt_template.format(
        pre_text=record.get("pre_text", ""),
        post_text=record.get("post_text", ""),
        table= record.get(table_key, "")
    )

    messages = [
        {"role": "system", "content": system_message_content},
        {"role": "user", "content": record.get("question", "")}
    ]
    return messages



def add_local_metric_column(
    df, 
    metric_func,
    gold_col="gold_answer",
    pred_col="model_answer",
    new_col_name="answer_exact_match"
):
    """
    Loops over df, calls metric_func(gold, pred), stores result in new_col_name.
    Returns a *copy* with that column added, to avoid SettingWithCopy issues.
    """
    df = df.copy()
    df[new_col_name] = None

    for i, row in df.iterrows():
        gold = row[gold_col]
        pred = row[pred_col]
        result = metric_func(gold, pred)
        df.at[i, new_col_name] = result

    return df

########





from src.llm import openai_llm

def add_llm_explanation_column(
    df,
    system_prompts_dict,
    model_name="gpt-3.5-turbo",
    gold_col="gold_answer",
    pred_col="model_answer",
    new_col_name="explanation_col",
    table = "table"
):
    """
    For each row, calls the LLM with a system prompt referencing gold_col & pred_col,
    stores the result in new_col_name.
    """
    df = df.copy()

    system_template = system_prompts_dict["system_prompt"]
    df[new_col_name] = None

    for i, row in df.iterrows():
        gold_val = row.get(gold_col,"")
        pred_val = row.get(pred_col,"")

        # Example user prompt:
        user_msg = (
            f"Gold: {gold_val}\n"
            f"Pred: {pred_val}\n\n"
            "Provide a short explanation or reasoning about their similarity/correctness."
        )

        # If your system prompt references placeholders for context:
        system_msg = system_template.format(
            pre_text=row.get("pre_text",""),
            post_text=row.get("post_text",""),
            table=row.get(table,"")
        )

        messages = [
            {"role":"system", "content":system_msg},
            {"role":"user", "content":user_msg}
        ]

        explanation = openai_llm(messages, model_name)
        df.at[i, new_col_name] = explanation
    
    return df




#####

# Structured outputs need slightly different requirements, therefore I've not adapted existing functions
# This would be future work
def process_records_struc_outputs(records, system_prompts, model_name,prompt_style, table_key, model_pred_col_name, StructuredResponse):
    """
    For each record, calls OpenAI and returns a DataFrame with columns:
      [id, question, gold_answer, program, table, html_table,
       <answer_col_name>, model, prompt_style, prompt]

    'model_pred_col_name' is the column under which the model's answer is stored.
    By default, it's 'model_answer', but you can override it (e.g. 'program_prediction').
    """
    results = []
    for r in records:
        # Build messages (unchanged)
        messages = construct_main_messages(r, system_prompts, table_key=table_key)
        try:
            response = openai.beta.chat.completions.parse(
                model=model_name,
                messages=messages,
                response_format=StructuredResponse
            )
            llm_answer = response.choices[0].message.parsed
        except Exception as e:
            llm_answer = f"Error: {e}"

        # Build the results row
        row_dict = {
            "id": r["id"],
            "pre_text": r["pre_text"],
            "post_text": r["post_text"],
            "gold_answer": r.get("gold_answer", ""),
            "program": r.get("program", ""),
            "html_table": r.get("html_table", ""),
            "question": r["question"],
            "model": model_name,
            "prompt_style": prompt_style,
            "prompt": system_prompts,  # or system_prompts["system_prompt"] if large
        }
        # Dynamically store the LLM’s answer in whichever column name was specified
        row_dict[model_pred_col_name] = llm_answer
        # print('here')
        # print(llm_answer.ans_pred)

        row_dict["model_answer"] = llm_answer.ans_pred
        row_dict[ "model_program_prediction"] = llm_answer.program_pred
        row_dict["model_reasoning"] = llm_answer.reasoning

        results.append(row_dict)

    return pd.DataFrame(results)




from src.llm import openai_llm_struc_resp

def add_llm_explanation_column_new(
    df: pd.DataFrame,
    system_prompt_template: str,
    gold_col: str = "gold_answer",
    pred_col: str = "model_answer",
    new_col_name: str = "explanation_col",
    model_name: str = "gpt-3.5-turbo"
) -> pd.DataFrame:
    """
    For each row in df, calls the LLM with gold_val, pred_val, and the system_prompt_template.
    Stores the resulting explanation in the 'new_col_name' column.

    Args:
        df: DataFrame containing at least 'gold_col' and 'pred_col'.
        system_prompt_template: A string that may contain '{gold}' and '{pred}' placeholders.
        gold_col: Column name for the gold (true) answer.
        pred_col: Column name for the predicted answer.
        new_col_name: Where we store the final LLM's explanation or evaluation.
        model_name: OpenAI model to use.

    Returns:
        A new DataFrame with an additional column ('new_col_name') containing the LLM responses.
    """
    df = df.copy()
    df[new_col_name] = None

    for i, row in df.iterrows():
        gold_val = row.get(gold_col, "")
        pred_val = row.get(pred_col, "")

        # Insert the row's gold/pred into the system prompt
        system_prompt = system_prompt_template['system_prompt'].format(gold=gold_val, pred=pred_val)

        # Build the messages for the ChatCompletion
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Call the LLM
        explanation = openai_llm(messages, model_name)
        df.at[i, new_col_name] = explanation

    return df