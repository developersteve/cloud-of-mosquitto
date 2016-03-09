#!/bin/bash

docker run --name mosquitto-pod-birdge \
-e K8S_API_SERVER_IP="<API_SERVER_IP>" -e K8S_API_SERVER_PORT="8080" \
-e POD_METADATA_NAME="mosquitto" \
kairen/mosquitto-pod-bridge:0.1.0
