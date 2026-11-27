# Interview guide

## One-minute explanation

“I built Net Probability to estimate the chance that a Premier League shot becomes a goal. I used a pinned 2026–27 snapshot covering 100 matches, validated the shot records and excluded penalties and own goals. The model uses shot distance, goal angle, body part and pre-shot context. I compared logistic regression and gradient boosting using chronological match-date splits, then built a dashboard with pitch maps, a probability simulator and SQLite queries running in the browser. The key result was that boosting won validation but logistic regression did better on test, so I kept the original selection and reported the reversal.”

## Questions you should be ready to answer

**Why not accuracy?** Goals are rare. Predicting “no goal” for every shot can give high accuracy but no useful probability ranking. Log loss and Brier evaluate probabilities; AUC evaluates ranking. Calibration asks whether shots assigned roughly 20% probability score about 20% of the time.

**How did you avoid leakage?** No provider xG, shot outcome, final score or post-shot location is a predictor. Entire kickoff dates stay together. Training preprocessing never sees validation or test data. The model is selected on validation, then evaluated on the later test block without tuning to its score.

**Why did the test winner differ?** Validation and test are small and cover different matches. A model can win on one sample without being universally superior. Switching the winner after seeing the test would turn the test set into another validation set. A future model decision needs new unseen data.

**What is xG?** A probability estimate based on the available shot features. Summing shot probabilities gives an expected goal total; it does not guarantee a score or prove finishing skill when a player exceeds it.

**How is geometry calculated?** Convert normalized locations to an assumed 105×68 m pitch. Calculate Euclidean distance to goal center and the angle between the two goalposts. The angle captures whether a location offers a wide or narrow view of goal.

**What does the bootstrap interval mean?** Resample whole test matches 300 times, preserving within-match shot groups. The percentile range describes sampling variation for a fixed model on this test population. It omits retraining uncertainty and source errors.

**Why browser SQLite?** It provides relational queries, a unique shot index, a team/date/player index and parameterized filtering without a database server. The trade-off is a downloadable, read-only snapshot rather than shared transactional storage.

**What would you improve?** Audit source identities against an authoritative licensed feed, obtain more seasons, use rolling out-of-time evaluation, consider calibration on a separate development block and add defender/goalkeeper information only when actual tracking coverage exists.

## Demo sequence

1. Explain the source snapshot and gameweek coverage.
2. Filter a team and match; inspect a shot's distance, angle and xG.
3. Choose Held-out test to distinguish evaluation from training predictions.
4. In Probability lab, move a hypothetical shot away from goal and change its body part. Explain that this uses the logistic baseline.
5. Show model evaluation and the validation/test reversal.
6. Open Data & methods, query SQLite and download an attributed export.

## Supported resume claims

- Engineered a reproducible xG pipeline for 2,712 non-penalty shots across 100 Premier League matches using Python, scikit-learn, geometric feature engineering and chronological match-separated evaluation.
- Validated a WebAssembly SQLite analytics dashboard with 20 automated tests, including cross-language prediction parity within 1e-8, and free GitHub Actions/Pages deployment .

Do not claim live tracking, complete season coverage, official data, commercial impact, or a test-winning boosted model. Explain AI assistance and your own contribution accurately when asked.
