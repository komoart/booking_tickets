FROM python:3.10-slim

ARG BUILD_TYPE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV POETRY_VERSION=1.4.0

RUN apt update && apt install -y \
  gcc \
  gettext \
  musl-dev \
  && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -U pip\

WORKDIR /movies_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]
