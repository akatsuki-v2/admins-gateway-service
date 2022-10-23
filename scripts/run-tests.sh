#!/usr/bin/env bash
set -eo pipefail

# don't generate .pyc files
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PYTHONPATH:/srv/root

cd /srv/root

pytest \
    --cov=app \
    --cov-report=term \
    --cov-report=html:tests/htmlcov \
    tests/
