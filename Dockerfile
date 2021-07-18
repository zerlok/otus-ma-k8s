ARG BASE_IMAGE=python:3.8-alpine3.13

FROM $BASE_IMAGE AS build

WORKDIR src

RUN apk add --no-cache gcc g++

# TODO: use poetry build tool
COPY requirements.txt ./
RUN pip install -r requirements.txt --target /build/

FROM $BASE_IMAGE AS main

WORKDIR src

RUN adduser -DH app && chown -R app:app /src/
USER app

COPY --from=build /build/ /build/
COPY src ./

ENV PYTHONPATH=/build/
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["-m", "echo"]
