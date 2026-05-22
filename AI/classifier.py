from AI.llm.setup import client

def classify(Prompt: str, model_name = "openrouter/free"): 

    # prompt formatting
    prompt = f"""
    
    You're given the following query: 
    {Prompt}

    this is the following way to categorize the given 

    Category,    Description,     Example Queries
    (1) Sales Performance, Questions about revenue, units, growth, and marketplace comparison, 'What were total sales for KLF Nirmal on Amazon in April?' / 'Which brand had the highest revenue last month?' / 'Compare Q1 vs Q2 sales for Cosmix'
    (2) Cross-Brand Portfolio, Comparative and aggregate questions across the entire brand portfolio, 'Rank all brands by net revenue this month' / 'Which marketplace generated the most returns last quarter?’

    based on the given categories Return ONLY:
        SALES_PERFORMANCE
        CROSS_BRAND_PORTFOLIO
        OUT_OF_SCOPE

    according the the query asked
    """

    # repsonse generation
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

