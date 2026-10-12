import re, sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
df = pd.read_parquet("data/processed/issues_outcome.parquet")
df = df.sort_values("created_at").reset_index(drop=True)
body = df["body"].fillna("")

df["title_words"] = df["title"].str.split().str.len()


def repro_chars(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    m = re.search(r"steps to reproduce:?", text, flags=re.I)
    if not m:
        return 0
    section = re.split(r"\n#{1,6} |does this issue occur|vs ?code version|os version",
                       text[m.end():], flags=re.I)[0]
    return len(re.findall(r"[^\W\d_]", section))


df["repro_chars"] = body.apply(repro_chars)
df["has_repro"] = (df["repro_chars"] >= 20).astype(int)
df["has_sysinfo"] = body.str.contains("os version", case=False).astype(int)

df["prior_reports"] = df.groupby("user").cumcount()
df["first_time"] = (df["prior_reports"] == 0).astype(int)

df["year"] = df["created_at"].dt.year
print(df[["has_repro", "has_sysinfo", "first_time"]].mean().round(3))
print(df.groupby("year")[["has_repro", "has_sysinfo", "first_time"]].mean().round(2))
print(df["title_words"].describe())

mask = body.str.contains("steps to reproduce", case=False) & (df["has_repro"] == 0)
print("heading but no real steps:", mask.sum())
for t in body[mask].head(3):
    print(t[:300].replace("\n", " | "))
    print("---")

df.to_parquet("data/processed/issues_features.parquet")