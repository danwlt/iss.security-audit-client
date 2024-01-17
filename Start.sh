#!/bin/bash

docker build -t my_client_app .

docker run -d -it --network=isssecurity-audit-backend_backend-network --name my_client_container my_client_app