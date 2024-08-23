FROM python:3.12.4-slim-bullseye AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git

WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml ./poetry.lock ./
RUN pip install --no-cache-dir --upgrade pip==24.1.1 \
    && pip install --no-cache-dir setuptools==70.2.0 wheel==0.43.0 \
    && pip install --no-cache-dir poetry==1.8.3

RUN poetry install --no-dev


FROM python-base AS development
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./src /app/src

EXPOSE 8000
CMD ["uvicorn", "src.presentation.api.main:init_api", "--workers", "4", "--host", "0.0.0.0", "--port", "8000", "--reload"]


FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./src /app/src

EXPOSE 8000
CMD ["python", "-Om", "src"]
