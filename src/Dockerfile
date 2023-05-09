FROM python:3.10 as builder

COPY pyproject.toml poetry.lock ./

RUN pip3 install poetry && poetry export -f requirements.txt -o requirements.txt

FROM  python:3.10 as runtime

WORKDIR /app

COPY --from=builder requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./
