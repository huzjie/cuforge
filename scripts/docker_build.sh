#!/usr/bin/env bash
# 构建并自检 Docker 镜像
set -e
docker build -t cuforge .
docker run --rm cuforge doctor
