# Devcontainer — AlphaTrace

Quick steps to open this repository in the devcontainer using VS Code:

1. Install Docker Desktop and the VS Code Remote - Containers extension.
2. In VS Code: Command Palette → Remote-Containers: Reopen in Container.

If you prefer to rebuild the container from the command line:

```bash
# from repository root
docker build -f .devcontainer/Dockerfile -t alphatrace-dev .
```

Post-create the container will attempt to install dev dependencies declared in `pyproject.toml`.

Troubleshooting:
- If `ruff` or `pyright` are not found, rebuild the container or run `pip install ruff pyright` inside the container.
