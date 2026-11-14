# CivicPulse AI

An original, runnable Python agent for **preliminary weather-hazard screening and mapped infrastructure context**. It retrieves live public data for a user-specified place and generates an evidence-linked report.

This repository is intentionally narrow: it does not claim to predict disasters, casualties, or resource requirements. It does not issue warnings or dispatch resources.

## What is implemented

- Open-Meteo Geocoding lookup for a place name.
- Open-Meteo current conditions and hourly forecast retrieval.
- OpenStreetMap Overpass lookup for nearby mapped hospitals, clinics, fire stations, and ambulance stations.
- Input/response validation and explicit source timestamps.
- A documented deterministic 0–100 screening indicator.
- CLI and FastAPI interfaces.
- Markdown report output.
- System-prompt export utility.
- Unit tests and opt-in live integration tests.

## Public data providers

- Open-Meteo Geocoding and Forecast APIs: https://open-meteo.com/en/docs
- OpenStreetMap data and Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- OpenStreetMap attribution: https://www.openstreetmap.org/copyright

Open-Meteo's free API is for non-commercial use; check its current terms before any commercial deployment. OpenStreetMap data is provided under the ODbL; provide attribution and review the share-alike obligations for your use.

The Overpass public service is shared infrastructure. Use it sparingly, cache results, and respect the instance's current usage policy. Do not use this project for bulk extraction.

## Requirements

- Python 3.10+
- Internet connection for live data retrieval
- No API key is required for the public Open-Meteo endpoints used here.
- Overpass is optional: if unavailable, the weather analysis still works and the report records the infrastructure source failure.

## Install on Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
cd civicpulse-ai
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH="$PWD/src"
```

## Run the tests

Offline unit tests use explicit mathematical test vectors only; they do not represent real-world observations or get included as live data.

```bash
pytest -q
```

Live API tests make actual HTTP requests and may fail if providers are offline, rate-limited, or the network is unavailable:

```bash
CIVICPULSE_LIVE_TESTS=1 pytest -q tests/test_live_sources.py
```

A live test failure must be reported as a provider/network failure, not hidden or relabelled as a pass.

## Run a real analysis

```bash
PYTHONPATH=src python -m civicpulse.cli analyze "Vijayawada, Andhra Pradesh, India" --radius 5000 --forecast-days 2 --output report.md
```

The command resolves the place through Open-Meteo, fetches the live forecast, attempts a bounded Overpass infrastructure query, computes the screening indicator, and writes a Markdown report.

Other examples:

```bash
PYTHONPATH=src python -m civicpulse.cli analyze "Warangal, Telangana, India" --output warangal-report.md
PYTHONPATH=src python -m civicpulse.cli analyze "Visakhapatnam, Andhra Pradesh, India" --forecast-days 3
```

Do not interpret the score as a government alert or a validated probability. The report includes its source timestamps and limitations.

## Run the API

```bash
PYTHONPATH=src uvicorn civicpulse.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` and use `POST /analyze` with:

```json
{
  "place": "Vijayawada, Andhra Pradesh, India",
  "radius_m": 5000,
  "forecast_days": 2
}
```

## OpenGAP integration

The root `agent.yaml`, `SOUL.md`, `RULES.md`, `DUTIES.md`, `AGENTS.md`, `EXPLAINABILITY.md`, `skills/`, and `tools/` are authored for this implementation. The manifest targets OpenGAP spec v0.1.0 and uses tool names without file extensions.

Install Node.js 18+ and the official CLI following the official OpenGAP documentation. Then, from this repository root:

```bash
npm install -g @open-gitagent/opengap
opengap validate
opengap info
opengap export --format system-prompt
```

The official CLI validation and export must be run locally before event submission. Save the actual terminal output. This package does not claim that the organizer's private Passport Control checks have already passed.

## Export and framework execution

A local system-prompt export can be generated with:

```bash
PYTHONPATH=src python -m civicpulse.cli export-system-prompt --output exports/civicpulse-system-prompt.md
```

This is a project-side prompt artifact, not proof of an OpenAI SDK or other external framework adapter. The event's Checkpoint 03 must be tested using the actual export adapter exposed by the official OpenGAP CLI and, where required, executed in the target framework. Do not claim an adapter visa until that real test succeeds.

## Reproducibility / evidence

For a submission evidence log, capture:
- `python --version`
- `pip freeze`
- `pytest -q`
- the actual CLI analysis output and report
- `opengap validate` output
- `opengap export --format system-prompt` output
- a fresh clone + install + repeat test

Never commit API credentials, personal data, or fabricated provider responses. Do not commit `.env` or runtime reports containing sensitive information.

## Scope and limitations

This is a first functional version, not a certified emergency-management system. It has no official alert feed, population exposure model, verified shelter inventory, route accessibility, hospital capacity, or ML model. Add those only after identifying authoritative data providers and implementing verifiable integrations.
