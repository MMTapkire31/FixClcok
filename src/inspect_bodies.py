import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
df = pd.read_parquet("data/processed/issues_outcome.parquet")
df["year"] = df["created_at"].dt.year
body = df["body"].fillna("")

print(body.str.len().describe())
print(body.str.contains("steps to reproduce", case=False).groupby(df["year"]).mean().round(2))
print(df.loc[df["year"] == 2024, "body"].dropna().iloc[3][:1200])
print("-----")
print(df.loc[df["year"] == 2018, "body"].dropna().iloc[3][:1200])