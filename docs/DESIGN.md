# Design decisions

Software: a football analytics application, not a marketing landing page.
Taste deal: cool-grey-cobalt and Instrument Sans / DM Mono, sharp controls. A neutral research surface lets shot locations and selection states carry the cobalt accent. Root tokens preserved. Main action: Filter shots. User-supplied name: Net Probability.

The dashboard uses a real pitch visualization, tabular evidence and four workspace views. Marketing-only fullscreen sections, decorative shader scenes and moving statistical plots would interfere with analytical comparison; they are not used. No stock photography, club logos or invented claims. Statistical axes, explanatory notes and data provenance remain visible.

Emil guidance: 160ms press/hover feedback, keyboard focus rings, native form controls, pointer-gated hover and reduced motion; analytical graphs update immediately. Color is accompanied by text/shape cues. Shot details are reachable through table buttons as well as pitch clicks.

Validation: Playwright covers functional views and widths 1440,1024,768,390,320. Final screenshots and Taste gate outcome to be recorded after checking the built application.

Taste finish gate: GATE: ERROR. Its local checker could not allocate ports5200–5299; layout checker also exited with an emitter error. Copy could not be checked because the dynamic page was not served. Following the skill's instruction, the gate was not rerun after ERROR. No gate pass is claimed. Independent production Playwright tests provide functional and responsive evidence.

Dependency review: Vite6.4.6 avoids known older dev-server issues. npm audit currently reports the picomatch<=4.0.7 ReDoS advisory through build-time glob dependencies; registry latest is4.0.7. The suggested downgrade to6.2.7 exposes additional Vite server advisories and was rejected. Vite is bound to127.0.0.1 locally and no dev server is deployed. Revisit the transitive advisory when a patch is available; do not process untrusted glob patterns.

Production verification completed: all7 Playwright checks passed in11.4s; screenshots reviewed at1440 and390 pixels, overflow checks also cover1024,768,320. Explicit accessible labels corrected an initial exact-label selector failure. Three JavaScript tests pass, including portable-model parity across2,712 shots within1e-8.
