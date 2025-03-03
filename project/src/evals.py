import pandas as pd

# Row level for match or not
def str_row_exact_match(gold, pred) -> int:
    return 1 if str(gold) == str(pred) else 0


def float_row_exact_match(gold: float, pred: str) -> bool:
    """
    Converts 'pred' (a string) to float, then checks if it exactly equals 'gold' (a float).
    If 'pred' cannot be parsed as float, returns False (rather than raising an error).
    Returns True if they match exactly, False otherwise.
    """
    try:
        pred_float = float(pred)
    except ValueError:
        # If 'pred' cannot be parsed as float, just return False
        return False
    
    # Return True only if they match exactly
    return pred_float == gold


### Used for answer 
# Aggregate level scoring for Exact match
def exact_match_score(df_data: pd.DataFrame, column_name: str) -> None:
    """
    Prints a correctness score for the column_name in df, which must contain 0/1 matches.
    """
    # Count the number of 1s (successful matches)
    correct_matches = df_data[column_name].sum()

    # Total number of rows
    total_rows = len(df_data)

    # Compute correctness score (percentage)
    em_score = (correct_matches / total_rows) * 100 if total_rows > 0 else 0

    return (f"Accuracy Score: {correct_matches}/{total_rows} ({em_score:.2f}%)")


# Build in fault tolerance 
def is_within_tolerance(gold: float, predicted: str, tolerance: float = 1e-2) -> bool:
    """
    Checks if the predicted value is within the allowed error range of the gold value.
    
    Args:
        gold (float): The correct/reference value.
        predicted (str): The model's predicted value (may be a string).
        tolerance (float): The acceptable margin of error (default: 1e-2).
    
    Returns:
        bool: True if the predicted value is within the allowed tolerance of the gold value, False otherwise.
    """
    if gold is None or predicted is None:
        return False  # Ensure both values exist before comparing

    # Convert predicted value to float
    try:
        pred_float = float(predicted)
    except ValueError:
        return False  # Return False if conversion fails

    return abs(gold - pred_float) <= tolerance



## Used for program 
def exact_match_score_numeric(df: pd.DataFrame, column: str) -> str:
    """
    Computes accuracy score for a binary column (1 = Equivalent, 0 = Not Equivalent).
    
    Args:
        df (pd.DataFrame): DataFrame containing evaluation results.
        column (str): Column with binary values (1 for correct, 0 for incorrect).

    Returns:
        str: Accuracy percentage.
    """
    # Convert column to numeric, handling errors
    df[column] = pd.to_numeric(df[column], errors='coerce')

    # Compute accuracy
    total = df[column].notna().sum()
    correct = df[column].sum()
    
    return f"Accuracy Score: {correct}/{total} ({(correct / total) * 100:.2f}%)" if total > 0 else "No valid data."

