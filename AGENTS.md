# Agent instructions

Build Net Probability for Premier League 2026–27. User authorizes public GitHub repository, free hosting, milestone commits, PRs and merges after checks. Keep work reproducible and update MEMORY.md at each milestone.

Never invent results or present incomplete season data as complete. Pin source snapshots and hashes, show coverage and attribution. Public availability is not an unrestricted license. Keep dataset terms distinct from source-code licensing.

Prevent target leakage: goal outcome is the target; provider xG, final score, post-shot endpoints and results are not predictors. Split by chronological match dates so matches and simultaneous dates never cross splits. Fit preprocessing on training only, choose models on validation only, evaluate held-out test once. Report logistic baseline and boosted model even if boosting loses. Exclude penalties and own goals from modeled population explicitly; do not hide exclusions. No tracking or defender features without actual coverage.

Use Python/scikit-learn, SQLite and a static browser dashboard, free GitHub Pages. Apply Taste/Emil design guidance adapted to analytical UI; accessible chart labels, filters, keyboard, reduced motion and responsive layouts. Use Playwright for browser checks. No API keys or paid services. Do not claim tests ran unless recorded.
