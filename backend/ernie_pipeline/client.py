
import os
import requests
import json
import logging

class ErnieClient:
    """
    Real client to talk to Novita AI's ERNIE 4.5 endpoint.
    Optimized for reliability with flaky networks.
    """
    def __init__(self):
        self.base_url = "https://api.novita.ai/v3/openai"
        # Use non-thinking model by default (faster, more reliable)
        self.model = os.getenv("NOVITA_MODEL", "baidu/ernie-4.5-vl-28b-a3b")
        self.fallback_model = "baidu/ernie-4.0-turbo-8k"
        self.api_key = os.getenv("NOVITA_API_KEY")
        
        if not self.api_key:
            logging.warning("NOVITA_API_KEY not found. ErnieClient will fail on calls.")

        self.session = requests.Session()
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        # Aggressive retry strategy for flaky networks
        retries = Retry(
            total=5,  # More retries
            backoff_factor=2,  # Longer waits
            status_forcelist=[429, 500, 502, 503, 504, 520, 524],
            allowed_methods=["POST"]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        
        logging.info(f"ErnieClient: model={self.model}, fallback={self.fallback_model}")

    def call(self, prompt: str, system: str = None, temperature: float = 0.3) -> str:
        """Call ERNIE API with automatic fallback and retries"""
        
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
            "temperature": temperature,
            "max_tokens": 4000
        }
        
        # Try primary model
        try:
            logging.info(f"Calling {self.model}...")
            response = self.session.post(
                f"{self.base_url}/chat/completions", 
                headers=headers, 
                json=payload, 
                timeout=120  # 2 minutes
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                if content and content.strip():
                    logging.info(f"✓ Success ({len(content)} chars)")
                    return content
            
            logging.warning(f"Primary failed: {response.status_code}")
        
        except requests.exceptions.Timeout:
            logging.error("Primary timed out (120s)")
        except Exception as e:
            logging.warning(f"Primary error: {e}")

        # Fallback
        logging.info(f"Trying fallback: {self.fallback_model}")
        payload["model"] = self.fallback_model
        
        try:
            response = self.session.post(
                f"{self.base_url}/chat/completions", 
                headers=headers, 
                json=payload, 
                timeout=90
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                if content and content.strip():
                    logging.info(f"✓ Fallback success ({len(content)} chars)")
                    return content
            
            raise RuntimeError(f"Fallback failed: {response.status_code}")
        
        except Exception as e:
            logging.error(f"Both models failed: {e}")
            raise RuntimeError(f"API unavailable: {e}")
