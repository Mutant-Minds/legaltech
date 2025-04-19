# Use the Python base image
FROM python:3.11-slim

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Environment variables for pip and poetry
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.7.1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry and pip dependencies
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir poetry==$POETRY_VERSION

# Copy the entire backend directory (including services and libs) into the container
COPY ./backend /app/backend

# Copy entrypoint scripts into the container
COPY ./docker/entrypoints /entrypoints

# Set the entrypoint for linting
ENTRYPOINT ["/bin/bash", "/entrypoints/run_test.sh"]
