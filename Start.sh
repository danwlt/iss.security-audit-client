#!/bin/bash

# Build the Docker image
docker build -t my_client_app .

# Run the Docker container and connect it to the 'backend-network'
docker run -d -it --network=audit-backend_backend-network --name my_client_container my_client_app