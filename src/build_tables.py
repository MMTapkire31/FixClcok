import os
import pandas as pd

NONFIX = {"*duplicate", "*out-of-scope", "*not-reproducible", "*as-designed",
          "*caused-by-extension", "*question", "*english-please", "*edu"}

df = pd.read_json("data/raw/vscode_bugs.jsonl", lines=True, convert_dates=False)
snapshot = pd.to_datetime(open("data/raw/snapshot.txt").read().strip(), utc=True)

df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
df["closed_at"] = pd.to_datetime(df["closed_at"], utc=True)

df["nonfix_label"] = df["labels"].apply(lambda ls: any(l in NONFIX for l in ls))
is_closed = df["state"] == "closed"

df["event"] = (is_closed & (df["state_reason"] == "completed")
               & ~df["nonfix_label"]).astype(int)

end = df["closed_at"].where(is_closed, snapshot)
df["duration_days"] = (end - df["created_at"]).dt.total_seconds() / 86400

print(df["event"].value_counts())
print(df["duration_days"].describe())
print("duration <= 0:", (df["duration_days"] <= 0).sum())

df["closed_year"] = df["closed_at"].dt.year
print(df[is_closed].groupby("closed_year")["nonfix_label"].mean().round(3))

os.makedirs("data/processed", exist_ok=True)
df.to_parquet("data/processed/issues_outcome.parquet")