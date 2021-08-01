ARG BASE_IMAGE=python:3.8-alpine3.13

FROM $BASE_IMAGE AS build

WORKDIR /build/
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apk add --no-cache \
        curl \
        gcc \
        g++ \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile=minimal && \
    source $HOME/.cargo/env && \
    pip install poetry==1.1.7

RUN adduser -D -h /build/ app
USER app

COPY pyproject.toml poetry.lock src/ ./
RUN poetry build -n && \
    pip install --target /build/libs/ dist/*.whl


FROM $BASE_IMAGE AS main

RUN adduser -DH app
USER app

COPY --from=build /build/libs/ /usr/local/lib/python3.8/site-packages/

ENV PYTHONOPTIMIZE=2
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["-m", "echo"]
