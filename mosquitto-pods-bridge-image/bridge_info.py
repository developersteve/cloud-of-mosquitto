# coding=utf-8
# Copyright 2016 NUTC i.m.a.c.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import os
import sys
import json
import requests


def main():
    k8s_ip = os.environ.get('K8S_API_SERVER_IP', "localhost")
    k8s_port = os.environ.get('K8S_API_SERVER_PORT', 8080)

    metedata_name = os.environ.get('POD_METADATA_NAME', "mosquitto")
    namespace = os.environ.get('POD_NAMESPACE', "default")

    url = "http://{0}:{1}/api/v1/namespaces/{2}/endpoints".format(
        k8s_ip,
        k8s_port,
        namespace,
    )
    try:
        response = requests.get(url)
        if "items" in response.json():
            my_item = None
            for item in response.json()["items"]:
                if metedata_name == item["metadata"]["name"]:
                    my_item = item
                    break

            if my_item is None:
                sys.exit("ERROR : Not find any metadata name")

            # print(json.dumps(my_item, indent=4, sort_keys=True))
            subsets = my_item["subsets"]

            container_infos = list()
            for subset in subsets:
                if "ports" not in subset:
                    sys.exit("ERROR : Not find any ports")

                port = subset["ports"][0]["port"]

                if "addresses" in subset:
                    for address in subset["addresses"]:
                        uid = str(address["targetRef"]["uid"]).split("-")
                        short_uid = uid[1] + uid[0]
                        container_infos.append({
                            "ip": address["ip"],
                            "uid": short_uid,
                            "resourceVersion": address["targetRef"]["resourceVersion"],
                            "port": port,
                        })

            my_ip = os.environ.get('HOST_IP', "localhost")
            container_infos = sorted(container_infos, key=lambda k: k['uid'])
            # print(json.dumps(container_infos, indent=4, sort_keys=True))

            connect_index = 0
            if len(container_infos) > 1:
                index = 0
                for info in container_infos:
                    if info["ip"] == my_ip:
                        connect_index = (index - 1) if (index - 1) > 0 else 0
                        break

                    index += 1

            if container_infos[connect_index]["ip"] != my_ip:
                connect_info = container_infos[connect_index]
                print("{0}:{1}".format(connect_info["ip"], connect_info["port"]))

    except Exception as e:
        print("ERROR :", "%s" % (e.__str__()))
        sys.exit()


if __name__ == '__main__':
    main()
