FROM python:3.10 as builder

WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
#RUN poetry install --only root
RUN poetry export -f requirements.txt >> requirements.txt


FROM  python:3.10 as runtime

RUN mkdir /app

COPY --from=builder /app/requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/routers ./routers
COPY src/database ./database
COPY src/main.py ./main.py
COPY src/alembic_inside.ini ./alembic.ini

#ENTRYPOINT ["alembic", "upgrade", "head", "&&", "uvicorn", "main:app", "--reload"]
#ENTRYPOINT ["uvicorn", "main:app"]
