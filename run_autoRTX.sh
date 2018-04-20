#!/bin/sh

CONTAINER_NAME="AutoRTX-python2.7"

OLD="$(docker ps --all --quiet --filter=name="$CONTAINER_NAME")"
if [ -n "$OLD" ]; then
    docker exec -it \
    ${CONTAINER_NAME} "$@"
else
  echo 'No such container!' 1>&2
  exit 1
fi