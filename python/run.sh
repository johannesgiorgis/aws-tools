#!/usr/bin/env bash

name="aws-tools-python:1.0"

# List Available Scripts
if [[ "$#" -eq 0 ]]
then
    docker container run --rm -v "${PWD}":/app -v ${HOME}/.aws:/root/.aws ${name} ls -ltFA /app | grep "aws.\+py" | sort -k9,9
    exit 0
fi

# docker container run --rm -v "$HOME/.aws":/root/.aws "$name" python aws-glue-list-crawlers.py -p default

docker container run --rm -v "${PWD}":/app -v "$HOME/.aws":/root/.aws "$name" python /app/${@}
