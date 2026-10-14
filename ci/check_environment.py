"""Fail before tests when the interpreter or locked dependency versions differ."""
from importlib.metadata import version
from pathlib import Path
import re
import sys

if sys.version_info[:2] != (3, 11):
    raise SystemExit('CI requires Python 3.11')
root = Path(__file__).resolve().parents[1]
lock = root / 'requirements-ci.lock' if (root / 'requirements-ci.lock').exists() else root / 'ci/requirements.lock'
for name, expected in re.findall(r'^([A-Za-z0-9_.-]+)==([^\s\\]+)', lock.read_text(), re.MULTILINE):
    actual = version(name)
    if actual != expected:
        raise SystemExit(name + ': locked ' + expected + ', installed ' + actual)
print('Python 3.11 / locked dependency versions verified')
