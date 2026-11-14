# Build and verification status

This status file records what was actually checked while assembling this source bundle.

## Verified in the build environment

- Python source compilation completed with `python -m compileall -q src tests`.
- Offline unit/API/manifest/report tests: **9 passed, 2 skipped** (the two live-provider tests are skipped unless explicitly enabled).
- The FastAPI application imports and exposes its routes.
- The project-side system-prompt artifact was generated from the actual `SOUL.md`, `RULES.md`, and `EXPLAINABILITY.md` files.
- The local test suite checks the root manifest's tool/skill file references, the event explainability headings, and separate Maker/Checker lines.

## Not verified in this build environment

- Live Open-Meteo and Overpass retrieval could not be verified here because outbound DNS/network access was unavailable. The live tests were attempted and failed at the network connection stage. This is not recorded as a provider success.
- The official OpenGAP CLI was not installed or run here. Therefore official `opengap validate`, official export results, and event-specific Passport Control checkpoints are **not claimed as passed**.
- No passport, visa, leaderboard points, or organizer approval is claimed.

## Required before submission

Run the live-source tests and an actual location analysis from the user's Ubuntu machine with internet access. Install the official OpenGAP CLI, run its validation and export commands, inspect the output, and submit the public GitHub repository to Passport Control. Preserve the actual output, including failures.
