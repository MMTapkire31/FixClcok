import pandas as pd

df = pd.read_json("data/raw/vscode_bugs.jsonl", lines=True, convert_dates=False)
closed = df[df["state"] == "closed"].copy()

stars = closed["labels"].explode()
print(stars[stars.str.startswith("*", na=False)].value_counts())

closed["is_dup_label"] = closed["labels"].apply(lambda ls: "*duplicate" in ls)
print(pd.crosstab(closed["state_reason"], closed["is_dup_label"]))

closed["closed_year"] = pd.to_datetime(closed["closed_at"], utc=True).dt.year
print(pd.crosstab(closed["closed_year"], closed["state_reason"]))