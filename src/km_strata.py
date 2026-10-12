import pandas as pd
from lifelines import KaplanMeierFitter

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")]

df["reporter_band"] = pd.cut(df["prior_reports"], [-1, 0, 4, 49, 100000],
                             labels=["first", "1-4 earlier", "5-49 earlier", "50+ earlier"])

for band, g in df.groupby("reporter_band", observed=True):
    print(band, "| n =", len(g), "| share with repro:", round(g["has_repro"].mean(), 2))
    for flag, name in [(1, "with"), (0, "without")]:
        s = g[g["has_repro"] == flag]
        if len(s) < 30:
            continue
        km = KaplanMeierFitter().fit(s["duration_days"], s["event"])
        print("   ", name, "n =", len(s), "median:", round(km.median_survival_time_, 1),
              "unfixed at 30d:", round(float(km.predict(30)), 3))