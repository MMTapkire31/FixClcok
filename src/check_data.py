import pandas as pd

df = pd.read_json("data/raw/vscode_bugs.jsonl", lines=True, convert_dates=False)
print("rows:", len(df))
df = df.drop_duplicates(subset="number")
print("after removing duplicates:", len(df))

df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
df["year"] = df["created_at"].dt.year
print(df["created_at"].min(), df["created_at"].max())
print(df.groupby("year").size())

print(df["state"].value_counts())
print(df["state_reason"].value_counts(dropna=False))

closed = df[df["state"] == "closed"]
print(closed["state_reason"].isna().groupby(closed["year"]).mean().round(2))