import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")].copy()
df["log_prior_reports"] = np.log1p(df["prior_reports"])
feats = ["has_repro", "has_sysinfo", "title_words", "first_time", "log_prior_reports"]

alt = df.copy()
alt["event"] = ((alt["state"] == "closed") & (alt["state_reason"] == "completed")).astype(int)

variants = {
    "baseline": df,
    "drop 2026 bugs": df[df["created_at"] < pd.Timestamp("2026-01-01", tz="UTC")],
    "from 2022 only": df[df["created_at"] >= pd.Timestamp("2022-01-01", tz="UTC")],
    "state_reason only": alt,
}

summaries = {}
for name, d in variants.items():
    m = CoxPHFitter().fit(d[feats + ["duration_days", "event"]], "duration_days", "event")
    summaries[name] = m.summary
    print(name, "| bugs:", len(d), "| fixes:", int(d["event"].sum()))

print()
print(pd.DataFrame({k: s["exp(coef)"] for k, s in summaries.items()}).round(3))
print()
for k, s in summaries.items():
    r = s.loc["has_repro"]
    print(k, "| has_repro HR CI:", round(r["exp(coef) lower 95%"], 3),
          "to", round(r["exp(coef) upper 95%"], 3))