#!/usr/bin/env bash
set -euo pipefail
python --version
python -m pip install -r requirements.txt
python -m pip install -r requirements/test-requirements.txt
export PYTHONPATH="$PWD/src"
pytest -q
