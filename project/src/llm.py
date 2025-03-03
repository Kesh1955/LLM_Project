import openai

def openai_llm(messages, model_name):
    """
    Basic wrapper to call OpenAI ChatCompletion.
    """
    try:
        resp = openai.chat.completions.create(
            model=model_name, 
            messages=messages)
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
    

def openai_llm_struc_resp(messages, model_name, StructuredResponse):
    """
    Structured output wrapper to call OpenAI ChatCompletion.
    """

    try: 
        completion = openai.beta.chat.completions.parse(
        model=model_name,
        messages=messages, 
        response_format=StructuredResponse,
        )

        return completion.choices[0].message.parsed
    except Exception as e:
            return f"Error: {e}"
