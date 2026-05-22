import os
from dotenv import load_dotenv
#from openai import OpenAI
from anthropic import Anthropic
load_dotenv()

key = os.getenv("key")

# setup for the LLM client
'''client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=key
)
'''
# claude
client = Anthropic(api_key = key)
