FROM python:3.8.2-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
