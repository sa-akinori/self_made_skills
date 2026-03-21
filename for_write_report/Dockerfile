FROM ubuntu:24.04

ARG USERNAME=researcher
ARG USER_UID=1000
ARG USER_GID=1000
ARG CLAUDE_CODE_VERSION=latest

ENV DEBIAN_FRONTEND=noninteractive

# System packages + Node.js + LaTeX + Japanese fonts + wkhtmltopdf
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Basic tools
    git \
    curl \
    wget \
    sudo \
    ca-certificates \
    gnupg \
    nano \
    # Python
    python3 \
    python3-pip \
    python3-venv \
    # LaTeX + Japanese fonts
    texlive-xetex \
    texlive-lang-japanese \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-science \
    latexmk \
    fonts-noto-cjk \
    fonts-ipafont \
    fonts-ipaexfont \
    # PDF tools (used by report-reviewer)
    poppler-utils \
    imagemagick \
    # Web page to PDF
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Node.js 22
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Python packages
RUN pip install --break-system-packages \
    google-genai \
    Pillow \
    matplotlib \
    seaborn \
    numpy \
    pandas

# Claude Code
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}

# Non-root user (Ubuntu 24.04 has 'ubuntu' user at UID 1000, reuse it)
RUN usermod -l ${USERNAME} ubuntu \
    && groupmod -n ${USERNAME} ubuntu \
    && usermod -d /home/${USERNAME} -m ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# Workspace
RUN mkdir -p /workspace && chown -R ${USERNAME}:${USERNAME} /workspace
WORKDIR /workspace

USER ${USERNAME}

ENV SHELL=/bin/bash
ENV EDITOR=nano

CMD ["bash"]