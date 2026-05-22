from AI.llm.setup import client

def extract(Prompt: str, cat: str, model_name = "openrouter/free"): 


    # prompt formatting
    prompt = f"""
    
    You're given the following prompt: 
    {Prompt}

    and the following category:
    {cat}

    if the category is OutofScope then terminate this request with the following message:  query cannot be answered with available data
    and do not return anything 

    else

    extract entities such as : brand name, marketplace, date range, metric, threshold
    Return ONLY valid JSON.
    """

    # response generation
    try:
        response = client.chat.completions.create(
                model = model_name,
                temperature = 0,
                messages = [
                    {
                        "role": "system",
                        "content": "You are an expert data analyst."
                        },
                    {
                        "role": "user",
                        "content": prompt
                        }
                    ])

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"error occured: {e}"

