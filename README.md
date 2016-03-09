# k8mosquitoo
k8mosquitoo 是 Kubernetes + Mosquitoo，主要透過 Kubernetes 來快速建置 Mosquitoo MQTT Broker 的 Bridge 叢集。

## Simple service bridge for Mosquitoo Broker
本部分將說明如何透過 Kubernetes 快速建立一個以 k8s-service 來讓多個 Mosquitoo Broker 服務進行共享 Topic（即 Bridge），首先我們要準備 Kubernetes 環境，接著透過指令來建置環境，使用檔案```k8s-service-bridge/mosquitto-bridge-svc.json```：
```sh
$ kubectl create -f k8s-service-bridge/mosquitto-bridge-svc.json
service "mosquitto-1" created
service "mosquitto-2" created
```

成功建立後，可以透過 k8s 指令查看：
```sh
$ kubectl get svc
NAME          CLUSTER_IP      EXTERNAL_IP   PORT(S)    SELECTOR      AGE
kubernetes    192.168.3.1     <none>        443/TCP    <none>        1m
mosquitto-1   192.168.3.192   nodes         1883/TCP   server-id=1   23s
mosquitto-2   192.168.3.154   nodes         1883/TCP   server-id=2   23s
```

接著要建立實際執行應用程式的環境，透過指令來建置環境，使用檔案```k8s-service-bridge/mosquitto-bridge-pods.json```：
```sh
$ kubectl create -f k8s-service-bridge/mosquitto-bridge-pods.json
pod "mosquitto-1" created
pod "mosquitto-2" created
```

完成建立後，即可透過 k8s 指令查看：
```sh
$ kubectl get pods -o wide
NAME          READY     STATUS    RESTARTS   AGE       NODE
mosquitto-1   1/1       Running   0          1m        10.21.20.201
mosquitto-2   1/1       Running   0          1m        10.21.20.195
```

若沒有問題，就可以透過 MQTT Client 進行測試，也可以到指定節點查看 broker 的容器 log 訊息：
```sh
$ docker logs <mosquitto_container_id>
address 192.168.3.192:1883
topic # both 0 bridge/ bridge/
bridge_protocol_version mqttv311
try_private true
```

## Simple pods bridge for Mosquitoo Broker
