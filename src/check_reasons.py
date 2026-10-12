import pandas as pd

df = pd.read_json("data/raw/vscode_bugs.jsonl", lines=True, convert_dates=False)
df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
df["year"] = df["created_at"].dt.year

print(pd.crosstab(df["year"], df["state_reason"].fillna("none (open)")))
print(df.groupby("year")["state"].apply(lambda s: (s == "open").mean()).round(3))

closed = df[df["state"] == "closed"]
print(closed["labels"].explode().value_counts().head(40))