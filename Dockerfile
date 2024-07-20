ARG SERVICE_NAME

FROM python:3.12-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

WORKDIR /usr/local/src/${SERVICE_NAME}


FROM base AS minio-api
RUN pip install fastapi pydantic pydantic_settings minio
COPY minio_microservice/main.py .
COPY minio_microservice ./minio_microservice

FROM base AS web
RUN apt-get update && apt-get install -y curl make
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . .

FROM ${SERVICE_NAME} AS final


