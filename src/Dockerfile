FROM python:3.10-slim as build-stage-1

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache poetry &&  \
    poetry export -f requirements.txt -o requirements.txt


FROM python:3.10-slim as build-stage-2

COPY --from=build-stage-1 requirements.txt ./
RUN pip install --no-cache --prefix=build -r requirements.txt

FROM  python:3.10-slim as runtime

WORKDIR /app
COPY --from=build-stage-2 build /usr/local
COPY src ./
