#!/bin/bash

# Stop and remove the Docker container
docker stop my_client_container
docker rm my_client_container

# Remove the Docker image
docker rmi my_client_app

