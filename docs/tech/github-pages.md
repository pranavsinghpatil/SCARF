# GitHub Pages Deployment

**Why GitHub Pages?**
It's free, fast, and integrates natively with our source code. Since SCARF generates **static** HTML/CSS/JS, we don't need a complex server like AWS or Heroku.

## 🚀 The Deployment Flow

1.  **Generate**: The Python backend creates a folder (e.g., `output/my-paper/`).
2.  **Commit**: We push this folder to a special branch (usually `gh-pages`).
3.  **Publish**: GitHub automatically serves that branch at `username.github.io/repo`.

## 🤖 Automation with Python

We don't ask the user to run git commands manually. We automate it using `gitpython` or subprocess calls.

```python
import subprocess
import os

def deploy_to_gh_pages(output_dir, repo_url, token):
    # 1. Clone the pages repo (shallow clone for speed)
    subprocess.run(["git", "clone", "--depth", "1", "--branch", "gh-pages", repo_url, "deploy_folder"])
    
    # 2. Copy new site files into it
    copy_tree(output_dir, "deploy_folder")
    
    # 3. Commit and Push
    os.chdir("deploy_folder")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Deploy new paper"])
    
    # Use the token for authentication
    auth_url = repo_url.replace("https://", f"https://{token}@")
    subprocess.run(["git", "push", auth_url, "gh-pages"])
```

## 🔑 Authentication

We use a **Personal Access Token (PAT)**.
*   The user provides this in `.env`.
*   Scope required: `repo` (to push to the repository).

## ⚠️ Challenges

### 1. Rate Limits
GitHub limits the number of builds per hour.
*   **Solution**: We debounce deployments or group multiple papers into one commit if possible.

### 2. Jekyll vs. No-Jekyll
By default, GitHub Pages runs Jekyll. This breaks folders starting with `_` (like `_static`).
*   **Fix**: We always add an empty `.nojekyll` file to the root of the output folder. This tells GitHub "Just serve the files, don't touch them."

### 3. Custom Domains
If the user has a custom domain, we need to preserve the `CNAME` file during deployment.
