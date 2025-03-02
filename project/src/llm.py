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
    
