import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test

df = pd.read_parquet("data/processed/issues_features.parquet")
df = df[df["created_at"] >= pd.Timestamp("2016-01-01", tz="UTC")].copy()
df["log_prior_reports"] = np.log1p(df["prior_reports"])

cols = ["duration_days", "event", "has_repro", "has_sysinfo",
        "title_words", "first_time", "log_prior_reports"]
cph = CoxPHFitter().fit(df[cols], duration_col="duration_days", event_col="event")

res = proportional_hazard_test(cph, df[cols], time_transform="rank")
res.print_summary(decimals=3)