#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
python3 ci/check_environment.py
python3 -m pip check
python3 -m unittest discover -s tests -v
