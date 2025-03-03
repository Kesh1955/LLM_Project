from pydantic import BaseModel, Field
from typing import List

class StructuredResponse(BaseModel):
    ans_pred: str = Field(description="The predicted answer to the question.")
    program_pred: str = Field(description= "A step-by-step symbolic program to precisely compute the final answer." 
                                        "For example: 'divide(a, b), multiply(#0, 10)." 
                                        "With placeholders (e.g., #0, #1) referencing previous steps.")
    reasoning: str = Field(description="Explanation of how the answer was derived.")