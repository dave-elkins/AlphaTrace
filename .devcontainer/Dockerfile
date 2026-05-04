FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV UV_VENV_CLEAR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libsqlite3-dev \
       git \
       curl \
       bash \
       procps \
       file \
       ca-certificates \
       gnupg \
       libbz2-dev \
       libncurses-dev \
       libssl-dev \
       libreadline-dev \
       zlib1g-dev \
       xz-utils \
       libffi-dev \
       liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

ARG USER=vscode
RUN useradd -m $USER || true

WORKDIR /workspace

RUN chown -R "$USER":"$USER" /workspace

# set Homebrew prefix and prepare directory as root
ENV NONINTERACTIVE=1
# Homebrew on Linux installs under /home/linuxbrew/.linuxbrew by default
ENV HOMEBREW_PREFIX=/home/linuxbrew/.linuxbrew
ENV PATH=$HOMEBREW_PREFIX/bin:$PATH
RUN mkdir -p $HOMEBREW_PREFIX || true

# The Homebrew installer uses a fixed default prefix on Linux (/home/linuxbrew/.linuxbrew).
# Create that prefix and make it writable by the non-root user so the installer can run.
RUN mkdir -p /home/linuxbrew/.linuxbrew && chown -R ${USER}:${USER} /home/linuxbrew/.linuxbrew || true

USER $USER

# install Homebrew as the non-root user (will use /home/linuxbrew/.linuxbrew)
RUN curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | /bin/bash -s

# activate and update brew as the non-root user
RUN eval "$($(/bin/ls -d /home/linuxbrew/.linuxbrew/bin 2>/dev/null || echo $HOMEBREW_PREFIX)/brew shellenv)" && brew update

# install beads, opencode, and other tools via homebrew
# Ensure brew environment is loaded in this RUN before invoking brew
RUN eval "$($HOMEBREW_PREFIX/bin/brew shellenv)" \
    && brew install beads \
    && brew install anomalyco/tap/opencode \
    && brew upgrade \
    && brew cleanup

# Install and Setup UV (https://astral.sh/uv/), a Python tool manager, and install some basic tools (ruff, pyright) for development.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && source $HOME/.local/bin/env \
    && uv self update \
    && echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc \
    && echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc \
    # Install basic dev tools (ruff, pyright)
    && uv tool install ruff \
    && uv tool install mypy \
    && uv tool install beads-mcp \
    # Create virtual environment used by UV
    && uv venv \ 
    && source .venv/bin/activate

CMD ["bash"]
