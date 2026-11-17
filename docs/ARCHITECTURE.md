# Architecture and acceptance criteria

Python reads the pinned event/fixture CSVs, validates identifiers/coordinates/outcomes, joins team names many-to-one, builds pre-shot geometry and categorical features, trains scikit-learn pipelines and writes SQLite and JSON. Browser assets use Vite and query SQLite through sql.js/WebAssembly. GitHub Actions regenerates artifacts and runs tests before Pages deployment.

Training features: distance to center, visible goal angle, shot body part, situation and preceding action. No player/team identity, provider xG or final outcome features. Labels use Goal versus other valid shot outcomes. Penalties/own goals excluded from model and clearly counted. Temporal partitions are by unique kickoff date; validation selects a model, untouched test provides final results. Dashboard may show frozen-model predictions on all data but must identify train/validation/test and only call test metrics held-out.

Done means: reproducible ingest and feature tests; no duplicate shot IDs or orphan fixtures; finite probabilities in [0,1]; all models and naive baseline reported; calibration bin counts; meaningful browser filter/map/export checks; visible source/season/coverage; verified live Pages URL; README/runbook/interview guide; milestone PRs merged.
