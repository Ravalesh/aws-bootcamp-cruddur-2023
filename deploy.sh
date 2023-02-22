#!/bin/sh

echo "Building the backend image"

docker build -t backend-flask ./backend-flask

echo "Deploying backend image"

docker run -itd -e FRONTEND_URL="https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" -e BACKEND_URL="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" -p 4567:4567 -v "/$(pwd)/backend-flask:/backend-flask" backend-flask

echo "building front end image"

docker build -t frontend-react-js ./frontend-react-js

echo "deploying frontend image"

docker run -itd -e REACT_APP_BACKEND_URL="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" -p 3000:3000 -v "/$(pwd)/frontend-react-js:/frontend-react-js" -v "/frontend-react-js/node_modules"  frontend-react-js

# exec "$@"