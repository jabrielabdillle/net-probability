# Project memory

User chose Net Probability, repository net-probability, focused on 2026–27 Premier League. Existing workflow authorizes public repo, free hosting, milestone PRs and merges. No extra confirmation needed for routine implementation.

Repository created: https://github.com/jabrielabdillle/net-probability
Local source is not a Git checkout; GitHub connector tree/commit/ref APIs publish milestone files because local git requires unavailable xcrun.

Source audit: pl-catalogue pinned at 5a9d2391d8cf1879a54c8a67bc25039c454479f0. Manifest exported 2026-11-10, reports 2,746 shots and GW1–10. Actual validation and model results pending. Data is third-party event data, not mock data; do not invent additional events. Provider rights and non-commercial attribution terms apply.

Next: validate source, implement pipeline and tests, then dashboard and publication. No model metrics or deployment yet.

M1 implementation: actual audit found 100 matches, 2,746 raw shots; excluded21 penalties +13 own goals. 2,712 modeled shots. Chronological train/validation/test counts1621/414/677. Boosting wins validation; logistic performs better on test, retained and documented. Python pipeline exports JSON/CSV/SQLite and portable logistic coefficients. See MODEL_CARD.md. Browser implementation in progress; not deployed.

M1 merged as PR #2 after CI passed. M2 browser validation complete: 7 Playwright checks passed; 3 JavaScript tests passed including all-shot sklearn parity within1e-8. Desktop/mobile screenshots reviewed. Pages source is configured as GitHub Actions. Dashboard PR and live deployment remain to finish. Taste gate ERROR is documented in docs/DESIGN.md.
