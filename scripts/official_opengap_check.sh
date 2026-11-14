#!/usr/bin/env bash
set -euo pipefail
command -v opengap >/dev/null 2>&1 || {
  echo "OpenGAP CLI is not installed. Install the official CLI before running this check." >&2
  exit 2
}
opengap validate
opengap info
opengap export --format system-prompt
