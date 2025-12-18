# Requests: The HTTP Client

**Role**: The bridge to the outside world.
SCARF uses `requests` to talk to:
1.  **Novita AI** (for ERNIE models).
2.  **GitHub API** (for deployment).

## 🛠 Best Practices

### 1. Timeouts (Critical!)
Never make a request without a timeout. If the API hangs, our server shouldn't hang forever.

```python
# Bad
requests.get('https://api.example.com')

# Good
requests.get('https://api.example.com', timeout=10)
```

### 2. Session Objects
We use `requests.Session()` to reuse TCP connections. This is much faster for multiple calls to the same host (like chatting with ERNIE).

```python
session = requests.Session()
session.headers.update({"Authorization": "Bearer ..."})

def chat(msg):
    # Reuses the connection established above
    return session.post(url, json=...)
```

### 3. Error Handling
We check status codes explicitly.

```python
try:
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status() # Raises HTTPError for 4xx/5xx
except requests.exceptions.Timeout:
    print("API is too slow!")
except requests.exceptions.HTTPError as err:
    print(f"API Error: {err}")
```

### 4. Retries
We combine `requests` with `urllib3`'s retry logic (or a custom decorator) to handle transient failures automatically.

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
```
