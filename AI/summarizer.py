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
        response = client.messages.create(
                model = model_name,
                max_tokens=1024,
                system = "You are an expert data analyst and HTML generator.",
                messages = [
                    {
                        "role": "user",
                        "content": prompt
                        }
                    ])

        return response.content[0].text.strip()

    except Exception as e:
        return f"error occured: {e}"


