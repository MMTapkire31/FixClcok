import json
from collections import Counter

with open("data/raw/test_issues.json") as f:
    issues = json.load(f)

first = issues[0]
print(list(first.keys()))
print(first["number"], first["title"])
print(first["state"], first["state_reason"], first["comments"])
print(first["user"]["login"], first["author_association"])
print([l["name"] for l in first["labels"]])

print(Counter(i["state"] for i in issues))
print(Counter(i["state_reason"] for i in issues))
print(min(i["created_at"] for i in issues), max(i["created_at"] for i in issues))