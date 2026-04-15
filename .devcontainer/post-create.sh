#/bin/bash

set -e

uv venv .venv
source .venv/bin/activate
uv sync --no-dev --no-install-project
uv sync --dev --no-install-project