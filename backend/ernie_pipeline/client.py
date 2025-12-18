
import os
import requests
import json
import logging

class ErnieClient:
    """
    Real client to talk to Novita AI's ERNIE 4.5 endpoint.
    Reference: docs/tech/ernie-api.md
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NOVITA_API_KEY")
        self.base_url = os.getenv("NOVITA_BASE_URL", "https://api.novita.ai/v1")
        self.model = "ernie-4.5" # or "ernie-5"
        
        if not self.api_key:
            logging.warning("NOVITA_API_KEY not found. ErnieClient will fail on calls.")

    def call(self, prompt: str, system: str = None) -> str:
        """
        Synchronous call to ERNIE.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1, # Low temp for reasoning
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.HTTPError as e:
            logging.error(f"ERNIE API Error: {e.response.text}")
            raise RuntimeError(f"ERNIE API Failed: {e}")
        except Exception as e:
            logging.error(f"ERNIE Network Error: {e}")
            raise e
