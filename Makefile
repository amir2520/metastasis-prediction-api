 # Make all targets .PHONY
.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

include .envs/.gcp
include .envs/.mlflow
include .envs/.uvicorn

export

SHELL = /usr/bin/env bash
USER_NAME = $(shell whoami)
HOST_NAME = $(shell hostname)
USER_ID = $(shell id -u)

ifeq (, $(shell which docker-compose))
	DOCKER_COMPOSE_COMMAND = docker compose
else
	DOCKER_COMPOSE_COMMAND = docker-compose
endif


CONTAINER_NAME = metastasis-fastapi-server
SERVICE_NAME = server


DOCKER_COMPOSE_RUN = $(DOCKER_COMPOSE_COMMAND) run --rm $(SERVICE_NAME)
DOCKER_COMPOSE_EXEC = $(DOCKER_COMPOSE_COMMAND) exec $(SERVICE_NAME)


guard-%:
	@#$(or ${$*}, $(error $* is not set))

build-for-dependencies:
	rm -f *.lock
	$(DOCKER_COMPOSE_COMMAND) build 

## Lock dependencies with poetry
lock-dependencies: build-for-dependencies
	$(DOCKER_COMPOSE_RUN) bash -c "if [ -e /home/$(USER_NAME)/poetry.lock.build ]; then cp /home/$(USER_NAME)/poetry.lock.build ./poetry.lock; else poetry lock; fi"

up: 
	$(DOCKER_COMPOSE_COMMAND) up 


down:
	$(DOCKER_COMPOSE_COMMAND) down


exec-in: up
	docker exec -it $(CONTAINER_NAME) bash


build:
	$(DOCKER_COMPOSE_COMMAND) build 


push: guard-IMAGE_TAG build auth
# 	@gcloud auth configure-docker us-east1-docker.pkg.dev --quiet

	@docker tag  "${DOCKER_IMAGE_NAME}:latest" "$${GCP_DOCKER_REGISTERY_URL}:$${IMAGE_TAG}"
	@docker push "$${GCP_DOCKER_REGISTERY_URL}:$${IMAGE_TAG}"


auth:
	gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin us-east1-docker.pkg.dev


deploy: push
	./scripts/create-server.sh


fastapi-tunnel:
	@echo "🔧 Setting up fastapi tunnel..."
	@gcloud projects add-iam-policy-binding end-to-end-ml-course-466603 \
		--member="user:$(shell gcloud config get-value account)" \
		--role="roles/iap.tunnelResourceAccessor" --quiet 2>/dev/null || true
	@gcloud compute firewall-rules create allow-ssh-iap \
		--direction=INGRESS --action=allow --rules=tcp:22 \
		--source-ranges=35.235.240.0/20 --quiet 2>/dev/null || true
	@gcloud compute instances add-tags "$${VM_NAME}" \
		--tags=allow-ssh-iap --zone "$${ZONE}" --quiet 2>/dev/null || true
	@gcloud compute ssh "$${VM_NAME}" --zone "$${ZONE}" --tunnel-through-iap -- -N -L "$${UVICORN_PORT}:localhost:$${UVICORN_PORT}"


