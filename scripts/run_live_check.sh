#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$PWD/src"
CIVICPULSE_LIVE_TESTS=1 pytest -q tests/test_live_sources.py
