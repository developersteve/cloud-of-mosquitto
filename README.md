# Cloud of Mosquitto
Cloud of Mosquitto is Kubernetes + Mosquitto, which is used to quickly build the Bridge cluster of Mosquitto MQTT Broker through Kubernetes.

## Simple service bridge for Mosquitto Broker
This section explains how to quickly create a top-level (ie Bridge) with k8s-service for multiple Mosquitto Broker services via Kubernetes. First we need to prepare the Kubernetes environment, then build the environment through the instructions, using the file k8s-service- Bridge/mosquitto-bridge-svc.json:

```sh
$ kubectl create -f k8s-service-bridge/mosquitto-bridge-svc.json
service "mosquitto-1" created
service "mosquitto-2" created
```

After successful establishment, you can view it through the k8s command:
```sh
$ kubectl get svc
NAME          CLUSTER_IP      EXTERNAL_IP   PORT(S)    SELECTOR      AGE
kubernetes    192.168.3.1     <none>        443/TCP    <none>        1m
mosquitto-1   192.168.3.192   nodes         1883/TCP   server-id=1   23s
mosquitto-2   192.168.3.154   nodes         1883/TCP   server-id=2   23s
```

Then create an environment where the application is actually executed, and build the environment through instructions, using the file k8s-service-bridge/mosquitto-bridge-pods.json:

```sh
$ kubectl create -f k8s-service-bridge/mosquitto-bridge-pods.json
pod "mosquitto-1" created
pod "mosquitto-2" created
```

Once the setup is complete, you can view it through the k8s command:
```sh
$ kubectl get pods -o wide
NAME          READY     STATUS    RESTARTS   AGE       NODE
mosquitto-1   1/1       Running   0          1m        10.21.20.201
mosquitto-2   1/1       Running   0          1m        10.21.20.195
```

If there are no problems, you can test through the MQTT Client, or you can view the broker's container log message at the specified node:
```sh
$ docker logs <mosquitto_container_id>
address 192.168.3.192:1883
topic # both 0 bridge/ bridge/
bridge_protocol_version mqttv311
try_private true
```

## Simple pods bridge for Mosquitto Broker
This section will explain how to build a bridge between Pods containers. First we need to prepare the Kubernetes environment, then build the environment through the instructions, using the file k8s-pods-bridge/mosquitto-bridge-svc.json:

```k8s-pods-bridge/mosquitto-bridge-svc.json```：
```sh
$ kubectl create -f k8s-pods-bridge/mosquitto-bridge-svc.json
service "mosquitto" created
```

After successful establishment, you can view it through the k8s command:
```sh
$ kubectl get svc
NAME         CLUSTER_IP     EXTERNAL_IP   PORT(S)    SELECTOR        AGE
kubernetes   192.168.3.1    <none>        443/TCP    <none>          16h
mosquitto    192.168.3.62   nodes         1883/TCP   run=mosquitto   20s
```

Then create an environment where the application is actually executed, and build the environment through instructions, using the file k8s-pods-bridge/mosquitto-bridge-rc.json:

```sh
$ kubectl create -f k8s-pods-bridge/mosquitto-bridge-rc.json
replicationcontroller "mosquitto" created
```

P.S Remember to modify the parameters in the file:

```sh
"env":[
  {
    "name": "K8S_API_SERVER_IP",
    "value": "localhost"
  },
  {
    "name": "K8S_API_SERVER_PORT",
    "value": "8080"
  },
  {
    "name": "BRIDGE_QOS",
    "value": "2"
  },
  {
    "name": "BRIDGE_TOPIC",
    "value": "bridge"
  },
  {
    "name": "POD_METADATA_NAME",
    "value": "mosquitto"
  },
  {
    "name": "POD_NAMESPACE",
    "valueFrom": {
      "fieldRef": {
        "apiVersion": "v1",
        "fieldPath": "metadata.namespace"
      }
    }
  }
]
```

After successful establishment, you can view it through the k8s command:

```sh
$ kubectl get rc,po -o wide
CONTROLLER   CONTAINER(S)   IMAGE(S)                            SELECTOR        REPLICAS   AGE
mosquitto    mosquitto      kairen/mosquitto-pod-bridge:0.1.0   run=mosquitto   2          2m

NAME              READY     STATUS    RESTARTS   AGE       NODE
mosquitto-eri9x   1/1       Running   0          2m        10.21.20.201
```

Use kubernetes to extend Container:

```sh
$ kubectl scale rc mosquitto --replicas=2
replicationcontroller "mosquitto" scaled
```

Then use the instructions to see if there is an extension:

```sh
$ kubectl get po -o wide
NAME              READY     STATUS    RESTARTS   AGE       NODE
mosquitto-5onyz   1/1       Running   0          1m        10.21.20.195
mosquitto-eri9x   1/1       Running   0          3m        10.21.20.201
```

Then go to the extended node and see if the Mosquitto Bridge of the Container has a Mosquitto broker that automatically connects to the previous Container:

```sh
$ docker logs <container_id>
connection mqttd
address 172.16.100.2:1883
topic # both 2 bridge/ bridge/
bridge_protocol_version mqttv311
try_private true
```
P.S currently has a limitation on Scale in, which needs to be removed from the first and last created Container.
