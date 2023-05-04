FROM python:3.10

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock

RUN poetry install --only root

COPY src/routers ./routers
COPY src/database ./database
COPY src/main.py ./main.py

ENTRYPOINT ["uvicorn", "main:app", "--reload"]
#ENTRYPOINT ["ls"]
