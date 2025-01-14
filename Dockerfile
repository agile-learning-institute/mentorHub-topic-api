FROM python:3.12.2-bookworm AS base
COPY /src .
COPY requirements.txt .

RUN python -m venv --copies .venv && \
    .venv/bin/pip install -r requirements.txt && \
    .venv/bin/pyinstaller --name main app/main.py

FROM debian:12.5 AS deploy

COPY --from=base /dist /opt

EXPOSE 8086
ENTRYPOINT ["/opt/main/main"]
