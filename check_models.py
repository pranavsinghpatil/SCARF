
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NOVITA_API_KEY")
url = "https://api.novita.ai/v3/openai/models"
headers = {"Authorization": f"Bearer {api_key}"}

try:
    response = requests.get(url, headers=headers, timeout=10)
    with open("models_log.txt", "w", encoding="utf-8") as f:
        if response.status_code == 200:
            data = response.json().get('data', [])
            f.write(f"Total Models: {len(data)}\n")
            
            ernie_models = [m['id'] for m in data if 'ernie' in m['id'].lower() or 'baidu' in m['id'].lower()]
            
            f.write(f"Ernie/Baidu Models Found: {len(ernie_models)}\n")
            for mid in ernie_models:
                f.write(f"MODEL: {mid}\n")
                
        else:
            f.write(f"Error: {response.text}\n")
except Exception as e:
    with open("models_log.txt", "w", encoding="utf-8") as f:
        f.write(f"Ex: {e}\n")
