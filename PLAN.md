# Software: football shot-quality research dashboard

## M0 — context and source audit
Create public repository, record source snapshot/terms, acceptance criteria, architecture and agent memory.

## M1 — reproducible modeling
Validate source records and fixture joins. Engineer distance and goal angle. Split chronological dates 60/20/20 (whole matches). Fit train-rate baseline, logistic regression and constrained gradient boosting. Select on validation log loss. Report test log loss, Brier, AUC, calibration and match-bootstrap intervals. Export SQLite, dashboard JSON and reproducible metrics. Test geometry, leakage, splits, ingestion and artifacts.

## M2 — interactive application
Shot map, team/player/match filters, probability inspection, comparisons, held-out evaluation, calibration and methods. No unlabelled in-sample performance. Functional/browser/responsive tests, production build.

## M3 — publication and explanation
Free Pages deployment, live smoke checks, interview guide, supported resume claims, final memory. Every milestone has commit, PR and authorized merge after checks.

## Completion
M0, M1 and M2 merged in PRs #1–#3. M3: Pages deployment succeeded and live overview/SQLite verified on 2026-11-27. Documentation and interview guide complete in the publication milestone PR. See docs/VALIDATION.md.
