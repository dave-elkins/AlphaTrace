FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libsqlite3-dev \
       git \
       curl \
       bash \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

ARG USER=vscode
RUN useradd -m $USER || true

WORKDIR /workspace

RUN chown -R "$USER":"$USER" /workspace

USER $USER

# Install and Setup UV (https://astral.sh/uv/), a Python tool manager, and install some basic tools (ruff, pyright) for development.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && source $HOME/.local/bin/env \
    && uv self update \
    && echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc \
    && echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc \
    # Install basic dev tools (ruff, pyright)
    && uv tool install ruff \
    && uv tool install pyright \
    # Create virtual environment used by UV
    && uv venv \ 
    && source .venv/bin/activate

RUN curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash

CMD ["bash"]
