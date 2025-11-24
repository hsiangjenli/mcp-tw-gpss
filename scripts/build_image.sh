#!/bin/bash

USERNAME="hsiangjenli"
IMAGE_NAME="$USERNAME/python-mcp-template"
date_tag=$(date +%Y-%m-%d)

docker build --no-cache -t $IMAGE_NAME:$date_tag -t $IMAGE_NAME:latest --push .