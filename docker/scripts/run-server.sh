#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

uvicorn metastatic.server:app --host 0.0.0.0 --port 8080
