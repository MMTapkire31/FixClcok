# FixClock: what predicts how fast VS Code bugs get fixed

**Data:** 46,636 bug-labeled issues from microsoft/vscode, Nov 2015 to
12 Oct 2026. The analysis uses the 46,201 created from 2016 on; 11,342 of
them (25%) are right-censored (still open, or closed without a fix).
**Method:** Kaplan-Meier curves and a Cox proportional hazards model, with
a "fix" defined as closed as `completed` with no non-fix label
(duplicate, out-of-scope, not-reproducible and similar).

## Findings

1. **Typical time to fix is 14.8 days (median)**, but the tail is long:
   an estimated 24% of bugs are still unfixed after a year.
2. **Who reports matters most.** Bugs from first-time reporters wait a
   median of about 78 to 108 days; bugs from reporters with 50+ earlier
   bug reports, about 4 days. In the model, a first-time reporter is
   associated with an 18% lower fix rate (HR 0.82, CI 0.79 to 0.85).
3. **Repro steps look bad in raw data and slightly good once adjusted.**
   Raw medians were 35 days with steps vs 10 without, but that gap mostly
   reflects who files the bug. Adjusted, repro steps go with a 6% higher
   fix rate (HR 1.06, CI 1.03 to 1.09). This is small, and it is not
   robust: using only 2022-onward bugs, the interval includes 1.
4. **Reporter experience helps mainly in the first two weeks.** Its effect
   is much weaker for bugs still open after 14 days. The model's
   constant-effect assumption fails for four of five features (it holds
   for repro steps), so single hazard ratios are averages.

## Prediction is modest

On bugs created in 2024 or later (never seen in training), the model's
concordance is 0.633. Reporter experience alone scores 0.635, so the other
features add almost no predictive power.

## What a team could do

- Give first-time reporters' bugs an explicit first-response target; they
  wait the longest.
- Don't mandate repro steps based on this analysis. The association is
  small and uncertain. Test the template change itself (before and after
  or an A/B comparison) before enforcing it.

## Limitations

- **Association, not causation.** Bug difficulty and affected component
  are not in the model.
- **Outcome definition:** `state_reason` was backfilled for older issues,
  so non-fix closures are identified through labels. Labels may be
  incomplete for recent closures.
- **Features are rough:** "repro steps" means a filled-in "Steps to
  Reproduce" section; steps written elsewhere count as none.
  "Reporter experience" counts earlier bug reports in this dataset only.
- **Only bug-labeled issues**; labels are added by maintainers, so
  unlabeled bugs are missing.
- **One repository.** Replication on TypeScript is the next step.