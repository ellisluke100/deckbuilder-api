FROM python:3.13-bullseye

ENV POETRY_VENV=/opt/poetry

# Install poetry and init the venv we will use for everything
RUN python3 -m venv ${POETRY_VENV} \
    && ${POETRY_VENV}/bin/pip install --upgrade pip \
    && ${POETRY_VENV}/bin/pip install poetry

WORKDIR /opt/code

# Copy dependencies
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN . ${POETRY_VENV}/bin/activate \
    && ${POETRY_VENV}/bin/poetry config virtualenvs.create false \
    && ${POETRY_VENV}/bin/poetry install --no-root \
    && ${POETRY_VENV}/bin/poetry update

# Copy code
COPY deckbuilder ./deckbuilder

EXPOSE 8000

# Entrypoint - run server
CMD ["/opt/poetry/bin/uvicorn", "deckbuilder.main:app", "--host", "0.0.0.0", "--port", "8000"]