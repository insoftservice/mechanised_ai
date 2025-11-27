from langchain_openai import ChatOpenAI  
import os

DEFAULT_LLM = {
    "model_name": "gpt-4.1",
    "temperature": 1
}

# NEW CODE ↓
API_KEY = os.getenv("OPENAI_API_KEY", None)

if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is not set. Please set the environment variable or insert your key directly."
    )

llm = ChatOpenAI(api_key=API_KEY, **DEFAULT_LLM)
