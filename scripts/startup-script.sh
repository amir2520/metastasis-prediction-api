#!/bin/bash

sleep 15


MLFLOW_TRACKING_URI=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mlflow_tracking_uri -H "Metadata-Flavor: Google")
UVICORN_PORT=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/uvicorn_port -H "Metadata-Flavor: Google")
GCP_DOCKER_REGISTERY_URL=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/gcp_docker_registery_url -H "Metadata-Flavor: Google")

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

echo '=========== Downloading Docker Image ============'
sudo gcloud auth configure-docker --quiet us-east1-docker.pkg.dev
echo "GCP_DOCKER_REGISTERY_URL = ${GCP_DOCKER_REGISTERY_URL}"
time sudo docker pull "${GCP_DOCKER_REGISTERY_URL}"

# systemctl stop jupyter

sudo docker run --init --network host --ipc host --user root --hostname "$(hostname)" --privileged \
  --log-driver=gcplogs \
  -e MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI}" \
  -e UVICORN_PORT="${UVICORN_PORT}" \
  ${GCP_DOCKER_REGISTERY_URL}