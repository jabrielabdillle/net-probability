# Deployment runbook

Public repository: https://github.com/jabrielabdillle/net-probability
Target website: https://jabrielabdillle.github.io/net-probability/
Host: free GitHub Pages; Settings → Pages → Source is GitHub Actions.

The browser job is pinned to Ubuntu 24.04 for Playwright 1.56.1 compatibility; ubuntu-latest moved to an unsupported OS. The web workflow installs locked Python dependencies, validates the pipeline, regenerates artifacts from committed pinned data, runs JS parity and Playwright tests, then publishes web/dist on main. PRs validate without publishing. Relative Vite URLs support the repository subpath. No credentials or runtime server are required.

Local build: `python -m src.pipeline`, then `cd web`, `npm ci`, `npm run build`. Generated public/data and dist are ignored; source snapshots are versioned. Deploy the built dist, not the source HTML shell.

For changes use a branch, run relevant checks, open a PR and merge after passing CI. The user authorized milestone merges. To undo a change, create a revert PR, validate and merge. For a404 check Pages source and the latest main deploy job; for missing data confirm the Python artifact step succeeded before Vite.

Dataset updates are explicit research versions: review source terms, pin a new commit, validate coverage/schema, preserve previous experiment metrics and define new chronological evaluation periods before looking at outcomes. Do not silently replace the test set or advertise weekly refreshes: there is no scheduled ingestion.

Dependency notes and current Taste checker limitation are in DESIGN.md. SQLite exports carry provenance; derived data remains subject to provider terms. Do not commercialize or relicense the dataset.

CI installs the pinned Chromium binary without --with-deps: the Ubuntu 24.04 hosted runner already supplies the required browser libraries. This avoids unrelated OS package upgrades on every deployment. If the runner image changes, inspect missing-library errors before changing this policy.
