import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")]
print("issues used:", len(df))

all_km = KaplanMeierFitter().fit(df["duration_days"], df["event"])
print("overall median days to fix:", round(all_km.median_survival_time_, 1))

fig, ax = plt.subplots(figsize=(8, 5))
for flag, name in [(1, "With repro steps"), (0, "Without repro steps")]:
    g = df[df["has_repro"] == flag]
    km = KaplanMeierFitter().fit(g["duration_days"], g["event"], label=name)
    km.plot_survival_function(ax=ax)
    still = [round(float(km.predict(d)), 3) for d in (1, 7, 30, 90, 365)]
    print(name, "| n =", len(g), "| median:", round(km.median_survival_time_, 1),
          "| still unfixed at 1/7/30/90/365 days:", still)

a = df[df["has_repro"] == 1]
b = df[df["has_repro"] == 0]
res = logrank_test(a["duration_days"], b["duration_days"], a["event"], b["event"])
print("log-rank p-value:", res.p_value)

ax.set_xlim(0, 365)
ax.set_xlabel("Days since the bug was reported")
ax.set_ylabel("Share still unfixed")
ax.set_title("VS Code bugs: time to fix, with vs without repro steps")
plt.tight_layout()
plt.savefig("memo_km_repro.png", dpi=150)
print("saved memo_km_repro.png")