# HiDevs Agent Passport — submission checklist

This checklist transcribes the visible event rules in the supplied Passport Control screenshots and maps them to this repository. It is not a guarantee of organizer approval.

## Selected track

**Track 01 — Custom Claw Workers** is the intended track: an original deployable domain worker. Submit only if the organizers confirm this track is still open and the repo meets its current rules. The screenshot says this track requires a write-up or demo. Prepare a genuine demo of the running API and live analysis.

## Checkpoint 01 — Validate

The screenshots require:

- `agent.yaml` in the repository root.
- `SOUL.md` in the repository root.
- `spec_version: "0.1.0"`.
- Agent name lowercase, hyphenated, and starting with a letter.
- Every listed tool and skill must exist.
- `DUTIES.md` and `AGENTS.md` must not place Maker and Checker on the same line.
- Checkpoint 01 must pass before the remaining checks run.

This repository includes root-level `agent.yaml`, `SOUL.md`, `DUTIES.md`, `AGENTS.md`, three tool definitions, and three skill directories. The test suite checks the local file references and the separate Maker/Checker lines. The official CLI and Passport Control must still be run by the submitter.

Commands:

```bash
PYTHONPATH=src pytest -q tests/test_manifest.py
npm install -g @open-gitagent/opengap
opengap validate
opengap info
```

## Checkpoint 02 — Explain

The screenshots require root-level `EXPLAINABILITY.md`, at least two sentences under each required heading, and the required words in the headings themselves. The headings are `Decision`, `Inputs`, and `Limits`.

Commands:

```bash
PYTHONPATH=src pytest -q tests/test_manifest.py
sed -n '1,220p' EXPLAINABILITY.md
```

Read the document and confirm that it describes the implementation that is actually present. Update it whenever the decision code or sources change.

## Checkpoint 03 — Export

The screenshots say the agent must run in a framework if it was not built in one; each export adapter is tested independently; at least one adapter must succeed; each successful export earns one visa.

This project exposes a FastAPI runtime. The local system-prompt artifact command is not proof of an official framework export. Install the official OpenGAP CLI and run its actual export command:

```bash
opengap export --format system-prompt
```

Then inspect the generated artifact and test the runtime/API. Keep the terminal output. Do not claim a visa until Passport Control confirms it. If attempting additional formats, run each one separately and preserve each result.

The event page lists these 15 visa targets: System Prompt, Claude Code, OpenAI SDK, CrewAI, OpenClaw, Nanobot, Lyzr, GitHub Models, GitHub Copilot, OpenCode, Cursor, Gemini, Codex, Kiro, and GitClaw. Availability and exact CLI format identifiers must be checked against the installed official CLI version; do not assume display labels equal CLI arguments.

## Functional tests

```bash
python --version
python -m pip install -r requirements.txt
python -m pip install -r requirements/test-requirements.txt
export PYTHONPATH="$PWD/src"
pytest -q
```

The unit tests use explicitly labelled mathematical test vectors to test calculations and file contracts. They are not presented as real-world observations or included as live data. Live-source tests are separate and make actual HTTP requests:

```bash
CIVICPULSE_LIVE_TESTS=1 pytest -q tests/test_live_sources.py
```

A live-source test can fail because of internet access, provider downtime, or rate limiting. Report that honestly.

## Real demonstration

```bash
PYTHONPATH=src python -m civicpulse.cli analyze "Vijayawada, Andhra Pradesh, India" --radius 1000 --forecast-days 1 --output /tmp/vijayawada-live-brief.md
cat /tmp/vijayawada-live-brief.md
```

This command makes live provider requests. It does not use a bundled sample dataset. A report is valid only if its source statuses show successful retrieval.

## API demonstration

```bash
PYTHONPATH=src uvicorn civicpulse.api:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"place":"Vijayawada, Andhra Pradesh, India","radius_m":1000,"forecast_days":1}'
```

## Clean-clone verification

After pushing the public repository, clone it into a new directory and repeat install, unit tests, live-source test, real analysis, official OpenGAP validation, and export. This verifies that the public repo—not an untracked local file—is complete.

## Evidence to retain

- GitHub repository URL and commit hash.
- Python and dependency versions.
- Complete pytest output.
- Actual live analysis output with source timestamps.
- API health and analysis responses.
- Official `opengap validate` output.
- Official export output and target-framework execution evidence.
- Passport Control checkpoint results and issued visa list.

Never edit logs to make a failed test look successful. Never include secrets in public evidence.
