# Net Probability

Premier League 2026–27 shot quality and expected-goals analytics. Explore shot maps, compare model probabilities, change hypothetical shot conditions and inspect chronological model evaluation.

**Website:** https://jabrielabdillle.github.io/net-probability/

## What this project does

- Validates a pinned third-party snapshot of 2,746 shots across 100 matches, August 21–November 8, 2026 (gameweeks 1–10).
- Excludes 21 penalties and 13 own goals, leaving 2,712 modeled shots.
- Engineers distance and goal angle; models pre-shot body part, situation and preceding action.
- Compares logistic regression, histogram gradient boosting, a training-rate baseline and external provider xG.
- Separates whole match dates chronologically; selects on validation log loss and reports held-out test results.
- Exports indexed SQLite, CSV, JSON and portable logistic coefficients.
- Serves a free static dashboard with pitch inspection, filters, probability scenarios, calibration and browser SQLite queries.

This is a partial-season research snapshot, not a live or official Premier League feed. Data comes from [pl-catalogue](https://github.com/oladeeayo/pl-catalogue), whose shot provider is Understat. Non-commercial attribution terms and upstream provider rights apply; see [data provenance](docs/DATA.md). No tracking data is used.

## Run it

Python 3.12 and Node 22 are used in CI.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock
python -m src.pipeline
python -m pytest -q
cd web
npm ci
npm run test:unit
npm run dev
```

For production browser checks:

```bash
cd web
npx playwright install --with-deps chromium
npm test
```

On macOS tests use installed Google Chrome; Linux CI uses Playwright Chromium. `npm test` builds the app and starts a local production preview.

## Model results

| Model | Test log loss ↓ | Test Brier ↓ | Test ROC-AUC ↑ |
|---|---:|---:|---:|
| Training goal rate |0.257266|0.065426|0.500000|
| Logistic regression |0.217407|0.057367|0.781594|
| Gradient boosting |0.222425|0.058883|0.765231|
| Provider reference |0.198591|0.054294|0.848413|

Boosting won validation and remains the selected explorer model; logistic regression performed better on test. The probability lab uses the portable logistic baseline and is labeled separately. Provider training data is unknown, so its score is context, not an independent benchmark.

Training/validation/test contain 1,621/414/677 shots from 59/16/25 matches. The held-out test period is October 25–November 8. Test metrics do not tune the model. Calibration includes bin counts; uncertainty intervals resample whole test matches 300 times. Details in the [model card](docs/MODEL_CARD.md).

## Validation and architecture

10 Python tests validate geometry, ingestion, exclusions, temporal separation and export integrity. Three JavaScript tests include portable-model agreement with sklearn across all 2,712 shots within 1e-8. Seven Playwright checks cover filters, model interaction, evaluation, SQLite/downloads, empty states, responsive layouts and loading recovery.

```text
Pinned source CSV + manifest
  → validation and fixture joins
  → pre-shot geometry + categorical features
  → chronological train / validation / test
  → sklearn models + calibration + match bootstrap
  → SQLite / JSON / CSV / portable logistic coefficients
  → Vite dashboard + sql.js WebAssembly
  → GitHub Actions → GitHub Pages
```

No backend, paid hosting account or API secret is required. SQLite runs in the browser as a read-only snapshot. Fonts load from Google Fonts with local fallbacks. Taste checker limitations and the remaining build-time dependency advisory are recorded in [design notes](docs/DESIGN.md).

## Project context

- [Agent instructions](AGENTS.md), [milestones](PLAN.md), [memory](MEMORY.md)
- [Architecture](docs/ARCHITECTURE.md), [data provenance](docs/DATA.md), [model card](docs/MODEL_CARD.md)
- [Deployment runbook](docs/DEPLOYMENT.md), [validation evidence](docs/VALIDATION.md)
- [Interview guide](docs/INTERVIEW_GUIDE.md)
