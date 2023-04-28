FROM python:3.10

WORKDIR /app

COPY ./routers ./routers
COPY ./database ./database
COPY main.py .

RUN pip install fastapi[all] "uvicorn[standard]"

ENTRYPOINT ["uvicorn", "main:app", "--reload"]