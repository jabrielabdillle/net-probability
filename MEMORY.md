# Project memory

Net Probability: Premier League 2026–27 shot quality and xG research.
Repository: https://github.com/jabrielabdillle/net-probability
Live: https://jabrielabdillle.github.io/net-probability/

User authorized public repo, free hosting, milestone commits, PRs and merges after checks. M0 blueprint merged in PR #1; M1 pipeline in PR #2; M2 dashboard in PR #3. M3 documentation records verified publication, maintenance and interview guidance.

Source: pl-catalogue / Understat, pinned at 5a9d2391d8cf1879a54c8a67bc25039c454479f0. Export dated 2026-11-10, covers gameweeks1–10 through November8. 2,746 raw shots /100 matches; 21 penalties and13 own goals excluded, leaving2,712 modeled shots. This is a third-party partial-season snapshot, not an official or live feed. Non-commercial attribution and provider terms apply.

Whole-date chronological training/validation/test:1,621/414/677 shots. Boosting selected on validation; logistic is better on test. Do not select again based on test results. Explorer uses boosting; probability lab explicitly uses logistic. No tracking features or provider xG inputs.

Validation:10 Python,3 JavaScript and7 Playwright checks passed locally and in CI. All-shot Python/JS logistic parity within1e-8. Screenshots reviewed at desktop/mobile; responsive checks cover320–1440px. Taste gate ERROR and build-time dependency advisory are in docs/DESIGN.md; do not claim a gate pass.

Pages deployment run44254329013 succeeded. On2026-11-27 public overview and SQLite verified:2,712 total and677 held-out test rows. Browser CI uses Ubuntu24.04 and installs Chromium without redundant system package upgrades.

Local source is not a Git checkout. GitHub connector tree/commit/ref APIs publish changes; local Git lacked xcrun. Future changes must start from current remote main, retain source provenance and use tested PRs. No paid services or secrets required. See docs/DEPLOYMENT.md and docs/INTERVIEW_GUIDE.md.
