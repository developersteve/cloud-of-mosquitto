#!/bin/bash

echo "${BRIDGE_BROKER_ID}"

if [ ! -z "$BRIDGE_BROKER_ID" ]; then

  hostName="MOSQUITTO_${BRIDGE_BROKER_ID}_SERVICE_HOST"
  portName="MOSQUITTO_${BRIDGE_BROKER_ID}_SERVICE_PORT_BROKER"
  BRIDGE_IP=$(echo ${!hostName})
  BRIDGE_PORT=$(echo ${!portName})
  sed -i 's/# address*/address ${BRIDGE_IP}:${BRIDGE_PORT}:/' /etc/mosquitto/mosquitto.conf
  echo "connection mqttd" >> /etc/mosquitto/mosquitto.conf
  echo "address ${BRIDGE_IP}:${BRIDGE_PORT}" >> /etc/mosquitto/mosquitto.conf
  echo "topic # both 0 bridge/ bridge/" >> /etc/mosquitto/mosquitto.conf
  echo "bridge_protocol_version mqttv311" >> /etc/mosquitto/mosquitto.conf
  echo "try_private true" >> /etc/mosquitto/mosquitto.conf

  cat /etc/mosquitto/mosquitto.conf
fi

/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
