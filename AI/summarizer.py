from AI.llm.setup import client

def summarize(data, model_name = "claude-sonnet-4-6"): 

    # prompt formatting
    
    prompt = f"""

            You are an analytics summarization assistant.

            SQL result data:
            {data}

            Generate a clean HTML fragment using ONLY:
            h3, p, table, tr, th, td

            Structure:
            - Direct Answer
            - Supporting Data
            - Interpretation
            - Source Attribution

            Rules:
            - Use INR formatting (₹1,24,500)
            - Use N/A for null or NoneType values
            - Maximum 10 table rows
            - Return ONLY HTML fragment
            - No markdown

            """

    # response generation
    try:
        with client.messages.stream(
            model=model_name,
            max_tokens=1024,
            system="You are an expert MariaDB SQL query generator.",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        ) as stream:
            for text in stream.text_stream:
                yield text 

    except Exception as e:
        yield f"error occured: {e}"


