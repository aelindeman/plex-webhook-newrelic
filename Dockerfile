FROM python:3.10-bullseye AS develop
WORKDIR /app
ENV PIP_CACHE_DIR=/tmp/pip \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_CACHE_DIR=/tmp/pypoetry \
    POETRY_VIRTUALENVS_CREATE=false
COPY . ./
RUN --mount=type=cache,target=/tmp/pip \
    --mount=type=cache,target=/tmp/pypoetry \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry install && \
    poetry build

FROM python:3.10-alpine
WORKDIR /app
COPY --from=develop /app/dist/app-*.whl /tmp/
RUN pip install /tmp/app-*.whl && \
    rm /tmp/app-*.whl
ENTRYPOINT ["/usr/local/bin/app"]
CMD []
