#!/bin/env python3
"""
  Description: Kubernetes pod resource calculator
  Author: Evgenii Semenov
"""
from kubernetes import client, config
import os

context = os.getenv("K8S_CONTEXT", "default")
prenamespaces = os.getenv("K8S_NAMESPACES", None)
if prenamespaces:
    namespaces = prenamespaces.split(",")
else:
    print("***ERROR** No namespaces were set!")
    exit(1)

delimiter = os.getenv("K8S_DELIMETER", ";")
cpu_units = {
    # "": 1.0,
    "Gi": 1.0,
    "G": 1.0,
    "m": 1000.0,
    "Mi": 1000.0,
    "M": 1000.0,
}

ram_units = {
    # "": 1.0,
    "Gi": 1.0,
    "G": 1.0,
    "m": 1024.0,
    "Mi": 1024.0,
    "M": 1024.0
}

_pods = []

config.load_kube_config()

configuration = client.Configuration()
configuration.api_key['authorization'] = os.getenv("K8S_BEARER_TOKEN", None)

v1 = client.CoreV1Api()
for namespace in namespaces:
    ret = v1.list_namespaced_pod(namespace)
    _pods = _pods + ret.items


def normalize(units, value):
    _key_ram = (k for k, v in units.items() if value.endswith(k))
    key_ram = next(_key_ram, None)
    if key_ram:
        return float(value[0:-len(key_ram):]) / units[key_ram]
    else:
        return float(value)


total_cpu = 0
total_ram = 0
print(f"namespace{delimiter}pod name{delimiter}CPU{delimiter}RAM, Gb;Comment")
for pod in _pods:
    name = pod.metadata.name
    namespace = pod.metadata.namespace
    containers = pod.spec.containers
    containers_cpu = 0
    containers_ram = 0
    comment = ""
    for container in containers:
        if not container.resources.limits:
            comment = f"No limits: {container.name}"
            continue
        containers_cpu = \
            containers_cpu + \
            normalize(cpu_units,
                      container.resources.limits["cpu"])
        containers_ram = \
            containers_cpu + \
            normalize(ram_units,
                      container.resources.limits["memory"])

    print(f"{namespace}{delimiter}{name}{delimiter}"
          f"{containers_cpu}{delimiter}{containers_ram}"
          f"{delimiter}{comment}")
    total_cpu = total_cpu + containers_cpu
    total_ram = total_ram + containers_ram

print(f"{delimiter}Total{delimiter}{total_cpu}{delimiter}{total_ram}")
