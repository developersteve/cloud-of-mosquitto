#!/bin/bash

echo "API Server : ${K8S_API_SERVER_IP}:${K8S_API_SERVER_PORT}"
echo "Metadata Name : ${POD_METADATA_NAME}"
echo "Metadata Namespace : ${POD_NAMESPACE}"

if [ ! -z "$K8S_API_SERVER_IP" ] && [ ! -z "$K8S_API_SERVER_PORT" ]; then

  HOST_IP=$(ip route get 8.8.8.8 | awk '{print $NF; exit}')
  BRIDGE_ADDRESS=$(python /opt/bridge_info.py)

  echo "connection mqttd" >> /etc/mosquitto/mosquitto.conf
  echo "address ${BRIDGE_ADDRESS}" >> /etc/mosquitto/mosquitto.conf
  echo "topic # both 0 bridge/ bridge/" >> /etc/mosquitto/mosquitto.conf
  echo "bridge_protocol_version mqttv311" >> /etc/mosquitto/mosquitto.conf
  echo "try_private true" >> /etc/mosquitto/mosquitto.conf

  cat /etc/mosquitto/mosquitto.conf
fi

/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
