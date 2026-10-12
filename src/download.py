import os, json, time
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

load_dotenv()
headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
           "Accept": "application/vnd.github+json"}
url = "https://api.github.com/repos/microsoft/vscode/issues"
OUT = "data/raw/vscode_bugs.jsonl"
PROGRESS = "data/raw/next_url.txt"
os.makedirs("data/raw", exist_ok=True)


def get_with_retry(u, params=None):
    for attempt in range(5):
        try:
            return requests.get(u, headers=headers, params=params, timeout=30)
        except requests.exceptions.RequestException as e:
            wait = 5 * (attempt + 1)
            print("network error, retrying in", wait, "s:", type(e).__name__)
            time.sleep(wait)
    return None


if os.path.exists(PROGRESS):
    next_url = open(PROGRESS).read().strip()
    params, mode = None, "a"
    print("resuming from saved position")
else:
    next_url = url
    params = {"state": "all", "labels": "bug", "per_page": 100}
    mode = "w"
    with open("data/raw/snapshot.txt", "w") as f:
        f.write(datetime.now(timezone.utc).isoformat())

kept, page = 0, 1
with open(OUT, mode, encoding="utf-8") as out:
    while next_url:
        r = get_with_retry(next_url, params)
        params = None
        if r is None or r.status_code != 200:
            print("stopped at page", page, "- run the script again to resume")
            break
        for i in r.json():
            if "pull_request" in i:
                continue
            row = {
                "number": i["number"], "title": i["title"], "body": i["body"],
                "created_at": i["created_at"], "closed_at": i["closed_at"],
                "state": i["state"], "state_reason": i["state_reason"],
                "user": i["user"]["login"],
                "author_association": i["author_association"],
                "comments": i["comments"],
                "labels": [l["name"] for l in i["labels"]],
            }
            out.write(json.dumps(row) + "\n")
            kept += 1
        out.flush()
        remaining = int(r.headers["X-RateLimit-Remaining"])
        print(page, kept, remaining)
        if remaining < 20:
            wait = int(r.headers["X-RateLimit-Reset"]) - time.time() + 5
            time.sleep(max(wait, 0))
        next_url = r.links.get("next", {}).get("url")
        if next_url:
            with open(PROGRESS, "w") as f:
                f.write(next_url)
        elif os.path.exists(PROGRESS):
            os.remove(PROGRESS)
        page += 1
        time.sleep(0.3)
print("done", kept)