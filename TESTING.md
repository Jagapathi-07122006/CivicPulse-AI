# Testing guide

## What the included tests prove

- `test_analyzer.py`: deterministic formula arithmetic, score caps, missing-data behavior, and labels using explicitly synthetic mathematical test vectors only.
- `test_report.py`: report content includes source and limitations disclosures.
- `test_manifest.py`: root manifest references existing skill/tool files, event explainability headings exist, and Maker/Checker are on separate lines.
- `test_live_sources.py`: opt-in tests that contact the real Open-Meteo and Overpass services.

The mathematical test vectors are not claimed as real weather observations, are not loaded by the agent, and are not included in generated reports. Live-source tests are kept separate so real external data retrieval is independently checked.

## Run offline unit tests

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements/test-requirements.txt
export PYTHONPATH="$PWD/src"
pytest -v
```

## Run live API tests

```bash
CIVICPULSE_LIVE_TESTS=1 pytest -v tests/test_live_sources.py
```

These tests do not substitute fixtures for live provider data. If the service is unreachable, the test reports the failure.

## Run a real location analysis

```bash
PYTHONPATH=src python -m civicpulse.cli analyze "Vijayawada, Andhra Pradesh, India" --radius 1000 --forecast-days 1 --output /tmp/civicpulse-brief.md
```

Check the report for all three provider/source records: geocoding, weather, and optional infrastructure. The infrastructure source can be unavailable without invalidating the weather result; the report must disclose that.

## Run the web API

```bash
PYTHONPATH=src uvicorn civicpulse.api:app --host 127.0.0.1 --port 8000
```

Use `/docs` for interactive API documentation.

## Official OpenGAP tests

```bash
npm install -g @open-gitagent/opengap
opengap validate
opengap info
opengap export --format system-prompt
```

The official CLI and organizer Passport Control are separate checks from this project's pytest suite. Save their actual output.
