#!/usr/bin/env bash

set -euo pipefail

# Create VM
gcloud compute instances create "${VM_NAME}" \
  --image "${IMAGE_NAME}" \
  --image-project "${IMAGE_PROJECT_ID}" \
  --boot-disk-auto-delete \
  --labels="${LABELS}" \
  --machine-type="${MACHINE_TYPE}" \
  --zone="${ZONE}" \
  --no-address \
  --network="${NETWORK}" \
  --subnet="${SUBNET}" \
  --scopes https://www.googleapis.com/auth/cloud-platform \
  --project="${GCP_PROJECT_ID}" \
  --metadata-from-file=startup-script=./scripts/startup-script.sh \
  --metadata \
gcp_docker_registery_url="${GCP_DOCKER_REGISTERY_URL}:${IMAGE_TAG}",\
mlflow_tracking_uri="${MLFLOW_TRACKING_URI}",\
uvicorn_port="${UVICORN_PORT}"
