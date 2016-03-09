## Dockerizing Mosquitto MQTT broker (Pods)
建置一個容器化的 MQTT Broker，並提供 Bridge 功能。該 Mosquitto MQTT broker 是部署於 Kubernetes 叢集上使用。支援了以下模式：
* Standalone Mode
* Bridged Mode

## 建置 Mosquitto 映像檔
首先 clone 下來專案，然後進入到```mosquitto-pods-images```，並透過 docker 指令來建置：
```sh
$ docker build -t kairen/mosquitto-pod-bridge .
```
