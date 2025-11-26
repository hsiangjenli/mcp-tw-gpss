#!/bin/bash

USERNAME="docker.io/hsiangjenli"
IMAGE_NAME="$USERNAME/mcp-tw-gpss"
date_tag=$(date +%Y-%m-%d)

docker build --no-cache -t $IMAGE_NAME:$date_tag -t $IMAGE_NAME:latest --push .