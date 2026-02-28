FROM python:3.11-slim

# OSパッケージ更新 + git install
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work_dir

COPY requirements.txt .

RUN pip install --upgrade pip
