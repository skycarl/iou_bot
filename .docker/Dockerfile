FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get -y install curl \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/tmp/poetry
RUN curl -sSL https://install.python-poetry.org/ | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN poetry config virtualenvs.create false \
  && poetry install --only main
