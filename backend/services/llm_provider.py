import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class LLMProvider:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    def is_configured(self):
        return bool(self.api_key)

    def get_embeddings(self):
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is missing.")
        return OpenAIEmbeddings(model="text-embedding-3-small")

    def get_chat_model(self):
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is missing.")
        return ChatOpenAI(model="gpt-4o", temperature=0)

    def get_dimension(self):
        return 1536
