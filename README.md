# iss.security-audit-client

## Requirements
- Docker

## Project setup
### Test it via Docker:
```RUN bash Start.sh```
```RUN docker exec -it my_client_container /bin/bash```
```RUN python3 main.py --level 1 [1 or 2]```
### Run on Ubuntu Server (urls need to be configured accordingly):
```RUN python main.py --level [1 or 2]```

## Depends on
- iss.security-audit-backend
- Docker Network: audit-backend_backend-network (if tested on docker)

## Information
- Make sure the .env URL matches the fast-api-backend host
- ARGS: Choose between level 1 or 2
- Testing on Docker will provide unwanted results due to the docker ubuntu image.