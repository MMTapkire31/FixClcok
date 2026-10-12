import json, os
import pandas as pd
from lifelines import KaplanMeierFitter

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")].copy()
df["band"] = pd.cut(df["prior_reports"], [-1, 0, 4, 49, 100000],
                    labels=["first", "1-4", "5-49", "50+"]).astype(str)

DAYS = [0, 1, 3, 7, 14, 30, 60, 90, 180, 365]
lookup = {}
for (band, rep), g in df.groupby(["band", "has_repro"]):
    km = KaplanMeierFitter().fit(g["duration_days"], g["event"])
    med = km.median_survival_time_
    lookup[f"{band}|{rep}"] = {
        "n": int(len(g)),
        "fixed_by": {str(d): round(1 - float(km.predict(d)), 4) for d in DAYS},
        "median_days": None if med == float("inf") else round(float(med), 1),
    }

os.makedirs("dashboard", exist_ok=True)
with open("dashboard/lookup.json", "w") as f:
    json.dump(lookup, f, indent=2)

print(len(lookup), "groups saved")
for k, v in lookup.items():
    print(k, "| n =", v["n"], "| median:", v["median_days"],
          "| fixed by day 30:", v["fixed_by"]["30"])