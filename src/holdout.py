import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")].copy()
df["log_prior_reports"] = np.log1p(df["prior_reports"])

CUTOFF = pd.Timestamp("2024-01-01", tz="UTC")
feats = ["has_repro", "has_sysinfo", "title_words", "first_time", "log_prior_reports"]

train = df[df["created_at"] < CUTOFF].copy()
test = df[df["created_at"] >= CUTOFF].copy()

days_to_cutoff = (CUTOFF - train["created_at"]).dt.total_seconds() / 86400
known = train["duration_days"] <= days_to_cutoff
train["event"] = ((train["event"] == 1) & known).astype(int)
train["duration_days"] = np.minimum(train["duration_days"], days_to_cutoff)

print("train bugs:", len(train), "| test bugs:", len(test))
for name, cols in [("all five features", feats),
                   ("reporter experience only", ["log_prior_reports"])]:
    use = cols + ["duration_days", "event"]
    m = CoxPHFitter().fit(train[use], "duration_days", "event")
    c_test = m.score(test[use], scoring_method="concordance_index")
    print(name, "| train:", round(m.concordance_index_, 3), "| test:", round(c_test, 3))