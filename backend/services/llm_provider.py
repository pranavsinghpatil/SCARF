import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class LLMProvider:
    def __init__(self):
        # DEFAULT TO GEMINI as per user request
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.api_key = os.getenv("GOOGLE_API_KEY") if self.provider == "gemini" else os.getenv("OPENAI_API_KEY")

    def is_configured(self):
        return bool(self.api_key)

    def get_embeddings(self):
        if self.provider == "gemini":
            if not os.getenv("GOOGLE_API_KEY"):
                raise ValueError("GOOGLE_API_KEY is missing. Please check backend/.env")
            return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        else:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY is missing. Please check backend/.env")
            return OpenAIEmbeddings(model="text-embedding-3-small")

    def get_chat_model(self):
        if self.provider == "gemini":
            if not os.getenv("GOOGLE_API_KEY"):
                raise ValueError("GOOGLE_API_KEY is missing. Please check backend/.env")
            # Updated to Gemini 2.5 Flash for 2026 context
            return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        else:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY is missing. Please check backend/.env")
            return ChatOpenAI(model="gpt-4o", temperature=0)

    def get_dimension(self):
        if self.provider == "gemini":
            return 768
        else:
            return 1536
