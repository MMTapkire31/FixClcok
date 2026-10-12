import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")].copy()
df["log_prior_reports"] = np.log1p(df["prior_reports"])

cols = ["duration_days", "event", "has_repro", "has_sysinfo",
        "title_words", "first_time", "log_prior_reports"]

cph = CoxPHFitter()
cph.fit(df[cols], duration_col="duration_days", event_col="event")
cph.print_summary(decimals=3)
print("concordance (on the same data it was fitted to):",
      round(cph.concordance_index_, 3)) 