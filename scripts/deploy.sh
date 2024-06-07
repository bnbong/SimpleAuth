#! /usr/bin/env sh

# Exit in case of error
set -e

IMAGE_NAME=${IMAGE_NAME?Variable not set}
TAG=${TAG?Variable not set}

docker build -t "${IMAGE_NAME}:${TAG}" .

# Docker Hub login (환경 변수로 로그인 정보 설정 필요)
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker push "${IMAGE_NAME}:${TAG}"
