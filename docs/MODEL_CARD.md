# Model card

Purpose: educational pre-shot goal probability estimates for the available Premier League 2026–27 compilation. Not an official feed or a betting recommendation. No tracking data or goalkeeper/defender positions are available.

Data: 2,746 raw events across 100 matches, 2026-08-21 through 2026-11-08. Exclude 21 penalties and 13 own goals, leaving 2,712 shots. Source own-goal records have missing provider xG; excluded records are counted before modeled-record xG validation. No missing xG is imputed.

Use normalized coordinates with assumed pitch dimensions 105×68m and goal width7.32m. Distance is to goal center. Goal angle is atan2(goal_width × forward_distance, forward_distance² + lateral_offset² − half_goal_width²). Standardize numeric features and one-hot encode body part, situation and preceding action using training-only preprocessing. Unknown categories encode as all-zero categorical vectors. Outcomes, scores, player/team identity and provider xG are excluded from inputs.

Unique kickoff dates split 60/20/20 by date count, not shot count. Training: 1,621 shots/59 matches (Aug21–Oct11). Validation:414/16 (Oct12–24). Test:677/25 (Oct25–Nov8). No same-date or same-match overlap. These are within-season chronological partitions; no earlier-season training data is claimed.

Fixed models: LogisticRegression C=1; HistGradientBoostingClassifier learning_rate=.05, max_iter=100, max_leaf_nodes=7, min_samples_leaf=30, l2_regularization=5, early_stopping=False. Seed42. Boosting selected by validation log loss. No refit and no test-driven tuning.

## Initial held-out results

| Model | Log loss | Brier | ROC-AUC |
|---|---:|---:|---:|
| Training base rate | .257266 | .065426 | .500000 |
| Logistic regression | .217407 | .057367 | .781594 |
| Gradient boosting (validation-selected) | .222425 | .058883 | .765231 |
| Provider reference | .198591 | .054294 | .848413 |

Boosting wins validation but logistic regression scores better on test. Report this reversal; do not retrospectively choose the test winner. Provider training data is unknown and may overlap; its numbers are contextual, not an independent benchmark. Metrics describe this pinned snapshot only.

Calibration uses fixed-width probability bins with counts; no post-hoc recalibration is fitted. Brier/log loss evaluate probability quality but are not pure calibration measures. Confidence intervals are percentile intervals from300 whole-match bootstrap draws, seed42, conditional on fitted models. They omit training uncertainty and future shifts.

The app identifies partitions; predictions shown on training records are in-sample. Player comparisons are descriptive, omit excluded shot types, and depend on source name labels. Goals−xG is not proof of finishing skill. Hypothetical scenarios use the logistic model, which may differ from the validation-selected model shown in the explorer.

References: [scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html), [histogram gradient boosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html), [source terms](https://github.com/oladeeayo/pl-catalogue).
