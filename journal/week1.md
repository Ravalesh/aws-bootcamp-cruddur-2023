# Week 1 — App Containerization

## Run the dockerfile CMD as an external script

I managed to run the dockerfile via external scipt.

here's the script I came up with:

```
#!/bin/sh

echo "Building the backend image"

docker build -t backend-flask ./backend-flask

echo "Deploying backend image"

docker run -itd -e FRONTEND_URL="https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" -e BACKEND_URL="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" -p 4567:4567 -v "/$(pwd)/backend-flask:/backend-flask" backend-flask

echo "building front end image"

docker build -t frontend-react-js ./frontend-react-js

echo "deploying frontend image"

docker run -itd -e REACT_APP_BACKEND_URL="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" -p 3000:3000 -v "/$(pwd)/frontend-react-js:/frontend-react-js" -v "/frontend-react-js/node_modules"  frontend-react-js

```

The above script is commited in the deploy.sh file of the root directory

I was successfully able to run both the backend and front end containers and both containers were able to communicate with each other.

![TASK1 1](../_docs/assets/week1/TASK1-01.JPG)

## Push and tag a image to DockerHub

I already had a docker account created long back.

I had to login to my docker account using the command:`docker login`

I build the backend image using the command: `docker build -t ravalesh/backend-flask:version-1 ./backend-flask`

I pushed the backend image using the command: `docker push ravalesh/backend-flask:version-1`

I build the frontend image using the command: `docker build -t ravalesh/frontend-react-js:version-1 ./frontend-react-js`

I pushed the frontend image using the command: `docker push ravalesh/frontend-react-js:version-1`

I was able to view my images in the docker hub

![DOCKER-PUSH-1.JPG 1](../_docs/assets/week1/DOCKER-PUSH-1.JPG)

Just to experiment, I installed docker desktop in my windows system and I ran the pushed image ocally on my system. I was successfully able to do so I was able to     get the responses from the flask server locally:

![DOCKER-PUSH-1.JPG 2](../_docs/assets/week1/DOCKER-PUSH-2.JPG)
  
## Use multi-stage building for a Dockerfile build

I managed to use multistage building for the flask-backend.

Here is the Dockerfile script  came up with:
```
FROM python:3.10-slim-buster as builder

WORKDIR /backend-flask

COPY requirements.txt requirements.txt

RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.10-slim-buster

COPY --from=builder /wheels /wheels

RUN pip install --no-cache /wheels/*

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

I created a new dockerfile named Dockerfile_multistaged and commited it to the root directory.
  
## Implement a healthcheck in the V3 Docker compose file
I implemented the health check for the backend and postgres and below is the docker-compose file with the health-check changes:

```
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      OTEL_SERVICE_NAME: 'backend-flask'
      OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
      OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4567/api/health_check"]
      interval: 10s
      timeout: 5s
      retries: 5
    depends_on:
      db:
        condition: service_healthy
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
      - /frontend-react-js/node_modules
    depends_on:
      backend-flask:
        condition: service_healthy
  dynamodb-local:
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
  db:
    image: postgres:13-alpine
    restart: always
    environment: 
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 1s
      timeout: 5s
      retries: 5


# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks: 
  internal-network:
    driver: bridge
    name: cruddur

volumes:
  db:
    driver: local
```

Now, the backend wouldn't start unless the postgress db was up and running. The frontend would not start unless the backend was up and running.

## Additional stuff

- I was successfully able to run the containers in my local system
- I added dockerignore files to ignore unnessary files from being added to the container.
