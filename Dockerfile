FROM andreisamofalov/poetry-python3

WORKDIR /app

ARG POETRY_GROUPS=--without=linters
COPY poetry.lock pyproject.toml ./
RUN poetry install ${POETRY_GROUPS} --no-interaction

COPY src ./
