#/bin/bash

set -e
 
# Create the virtual environment only if it doesn't already exist
if [ ! -d ".venv" ]; then
	uv venv .venv
fi

source .venv/bin/activate
uv sync --no-dev --no-install-project
uv sync --dev --no-install-project