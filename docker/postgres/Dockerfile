# syntax=docker/dockerfile:1

ARG POSTGRES_IMAGE=postgres:18-bookworm
FROM --platform=$TARGETPLATFORM ${POSTGRES_IMAGE}

ARG PGVECTOR_VERSION=v0.8.3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ca-certificates \
    postgresql-18-postgis-3 \
    postgresql-18-postgis-3-scripts \
    postgresql-server-dev-18 \
    && git clone --branch "${PGVECTOR_VERSION}" --depth 1 https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make clean \
    && make OPTFLAGS="" \
    && make install \
    && cd / \
    && rm -rf /tmp/pgvector \
    && apt-get purge -y --auto-remove build-essential git postgresql-server-dev-18 \
    && rm -rf /var/lib/apt/lists/*

COPY init.sql /docker-entrypoint-initdb.d/10-extensions.sql
