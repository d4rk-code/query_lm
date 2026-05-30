from AI.llm.setup import client
from AI.memory import history
#from AI.classifier import classify
#from AI.entity_extractor import extract
#free model: openai/gpt-oss-20b:free

def query_generator(Prompt: str, model_name = "claude-sonnet-4-6"): 

    '''
    cat = classify(Prompt)

    if cat == "OUT_OF_SCOPE":
        return "query can't be answered with the current data"

    entities = extract(Prompt, cat)
    '''

    # prompt formatting 

    context = ""

    if history:
        max_context = len(history)
        recent_context = history[-max_context:]


        for item in recent_context:
            context += f"""

                    Previous context for the user: 

                    Question:
                    {item["question"]}

                    SQL:
                    {item["sql"]}

                    Summary:
                    {item["response"]}

                    """

    prompt = f"""

    You are an expert MariaDB SQL query generator.

    {context}

    User Request: 
    {Prompt}

    Generate ONLY a valid MariaDB SQL query.

    STRICT RULES:
    - Output ONLY valid MariaDB SQL.
    - Do not explain anything.
    - Do not use markdown.
    - Always end the query with a semicolon.
    - Use ONLY the provided table and columns.
    - Do NOT invent tables.
    - Do NOT invent columns.
    - Simple aliases using AS are allowed.
    - Use valid MariaDB syntax ONLY.
    - Use MONTH(ORDER_DATE) for month filtering.
    - Revenue calculations should use:
      OUTWARD_QTY * OUTWARDSKU_SELLING_PRICE_EXCL_TAX
    - They are NOT database columns.
    - Prefer simple queries over complex joins.

    DATABASE SCHEMA

    Table:
    tbl_sales_data_mart

    Order Information:
    - DISPLAY_ORDER_CODE TEXT
    - ORDER_DATE DATE
    - ORDER_RECEIVED_DATE DATE
    - ORDER_STATUS TEXT
    - ITEM_STATUS TEXT

    Product Information:
    - LISTING_SKU TEXT
    - ASIN TEXT
    - PRODUCT_TYPE TEXT
    - LISTINGPRODUCTNAME TEXT
    - LISTINGPRODUCTSHORTNAME TEXT
    - BRAND_NAME TEXT
    - CATEGORY_NAME TEXT

    Pricing & Revenue:
    - RECEIVED_QTY INTEGER
    - LISTINGSKUMRP FLOAT
    - LISTING_SELLING_PRICE FLOAT
    - OUTWARD_QTY INTEGER
    - OUTWARD_MRP FLOAT
    - OUTWARDSKU_SELLINGPRICE_ORIGINAL FLOAT
    - OUTWARDSKU_SELLINGPRICE_DERIVED FLOAT
    - OUTWARDSKU_SELLING_PRICE_EXCL_TAX FLOAT
    - TAX_RATE FLOAT

    Marketplace & Vendor:
    - MARKETPLACE TEXT
    - SALES_CHANNEL TEXT
    - VENDOR_NAME TEXT

    Location:
    - CITY TEXT
    - STATE TEXT
    - country TEXT
    - zone TEXT

    """
    # response generation
    try:
        response = client.messages.create(
                model=model_name,
                max_tokens=1024,
                # FIX: Pass the system prompt as a direct, top-level keyword argument
                system="You are an expert MariaDB SQL query generator.",
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                        }
                    ]
                )

        print(response)

        # Ensure the response object itself exists
        if not response:
            return "error occured: empty response"

        # Claude stores chunks in a 'content' attribute list instead of 'choices'
        if not getattr(response, 'content', None):
            return "error occured: no content blocks returned"

        # Grab the first block of content
        first_block = response.content[0]

        # Claude supports multi-modal blocks, so we verify it's a text block
        if getattr(first_block, 'type', None) != 'text':
            return "error occured: first content block is not text"

        # Extract the raw string data
        content = first_block.text

        if not content:
            return "error occured: empty content string"

        return content.strip()

    except Exception as e:

        return f"error occured: {e}"
