# Validation evidence

M0 blueprint merged as PR #1. M1 pipeline merged as PR #2 after Analytics checks passed. Ten local Python tests passed; exports contain 2,712 modeled events from 2,746 raw records. 34 excluded records are explicitly counted. The model card records the initial metrics and chronological split boundaries.

M2 local production build succeeded. Three JS tests passed, including sklearn parity within 1e-8 for every exported shot. Seven Playwright checks passed in 11.4 s. The initial exact-label failure was fixed with explicit accessible control labels. Desktop/mobile screenshots were reviewed, with overflow checks at 1440,1024,768,390,320 pixels. Dashboard PR #3 merged after all CI checks passed in run 44254078509.

Taste gate returned ERROR because its local server could not allocate a port; no pass is claimed. See DESIGN.md for the full limitation and dependency advisory.

M3 publication: [Pages deployment run 44254329013](https://github.com/jabrielabdillle/net-probability/actions/runs/44254329013) succeeded for main commit `95dcaa7225eee389fc51e3145d55855648ef63ff`. On 2026-11-27, verified the public dashboard loads and its browser SQLite query returns 2,712 total records and 677 held-out test records. The gameweek1–10 coverage notice is visible.

The initial dashboard CI run failed before browser tests because ubuntu-latest used Ubuntu 26.04, unsupported by the locked Playwright version. The workflow now pins Ubuntu 24.04.

The runner package installation was slow; using its existing browser libraries and installing only the pinned Chromium binary resolved the setup delay. All dashboard CI checks then passed.
