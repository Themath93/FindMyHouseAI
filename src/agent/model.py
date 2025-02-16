from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_openai_model(model: str ="gpt-4o-mini"):
    return ChatOpenAI(model=model)