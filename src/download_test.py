import os, json, time
import requests
from dotenv import load_dotenv

load_dotenv()
headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
           "Accept": "application/vnd.github+json"}
url = "https://api.github.com/repos/microsoft/vscode/issues"

all_issues = []
for page in range(1, 4):
    params = {"state": "all", "labels": "bug", "per_page": 100, "page": page}
    r = requests.get(url, headers=headers, params=params)
    batch = [i for i in r.json() if "pull_request" not in i]
    all_issues.extend(batch)
    print(page, len(batch))
    time.sleep(0.5)

os.makedirs("data/raw", exist_ok=True)
with open("data/raw/test_issues.json", "w") as f:
    json.dump(all_issues, f)
print("saved", len(all_issues))