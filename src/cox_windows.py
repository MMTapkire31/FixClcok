import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")].copy()
df["log_prior_reports"] = np.log1p(df["prior_reports"])
feats = ["has_repro", "has_sysinfo", "title_words", "first_time", "log_prior_reports"]
CUT = 14

early = df.copy()
early["event"] = ((early["event"] == 1) & (early["duration_days"] <= CUT)).astype(int)
early["duration_days"] = early["duration_days"].clip(upper=CUT)

late = df[df["duration_days"] > CUT].copy()
late["duration_days"] = late["duration_days"] - CUT

for name, d in [("FIRST 14 DAYS", early), ("AFTER DAY 14", late)]:
    m = CoxPHFitter().fit(d[feats + ["duration_days", "event"]], "duration_days", "event")
    print(name, "| bugs:", len(d), "| fixes:", int(d["event"].sum()))
    print(m.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%"]].round(3))
    print()