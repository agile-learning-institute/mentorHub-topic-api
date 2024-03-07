FROM python:3.12.2-bookworm AS base
COPY /src .
COPY requirements.txt .

RUN python -m venv --copies .venv && \
    .venv/bin/pip install -r requirements.txt && \
    .venv/bin/pyinstaller --name main app/wsgi.py

FROM python:3.12.2-bookworm AS deploy

COPY --from=base /dist /opt

EXPOSE 8086
CMD ["/opt/main/main"]
