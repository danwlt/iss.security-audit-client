# Use an official Python runtime as a parent image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3

RUN apt-get install -y python3-pip

RUN pip install requests

RUN pip install python-dotenv

COPY main.py /app

COPY .env /app