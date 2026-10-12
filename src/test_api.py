import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

url = "https://api.github.com/repos/microsoft/vscode/issues"
headers = {"Authorization": f"Bearer {token}",
           "Accept": "application/vnd.github+json"}
params = {"state": "all", "per_page": 5}

r = requests.get(url, headers=headers, params=params)
print(r.status_code)
print(r.headers["X-RateLimit-Remaining"])
for issue in r.json():
    print(issue["number"], issue["state"], issue["created_at"],
          issue["closed_at"], "pull_request" in issue)