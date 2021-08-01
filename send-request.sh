#!/bin/bash

CLUSTER_IP=$(minikube ip)

request() {
  path=${1:-"/"}
  shift 1

  curl -s \
    -X GET \
    -H 'host: arch.homework' \
    -H 'content-type: application/json' \
    "http://${CLUSTER_IP}/otusapp/d.troshnev${path}" \
    "${@}"
  echo
}

request /health

request
request / --data-raw '{"hello": "world"}'
