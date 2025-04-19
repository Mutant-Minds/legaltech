FROM tiangolo/uvicorn-gunicorn-fastapi:latest AS builder

WORKDIR /app/

# Environment variables for pip and poetry
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.7.1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry and pip dependencies
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir poetry==$POETRY_VERSION pipenv cryptography==3.3 \
  && poetry config virtualenvs.create false

# Copy project files
COPY services/globdoc/pyproject.toml .
COPY services/globdoc/poetry.lock .
COPY ./libs ./libs

# Update path in pyproject.toml to match the Docker structure i.e. adjust dependency path
RUN sed -i 's#specter = {path="../../libs/specter"}#specter = {path="./libs/specter"}#' pyproject.toml

# Install dependencies
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Copy source code
COPY services/globdoc/src/ .
COPY services/globdoc/docs/ ./docs

# expose ports!
EXPOSE 8080

# Optional Healthcheck
# HEALTHCHECK --interval=30s --timeout=5s CMD curl --fail http://localhost:8080/health || exit 1

# Start service.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
