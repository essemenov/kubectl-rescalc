# k8s namespace resource calculator tool

This is small tool to output containers limits in k8s using access token.

## Requirements
* Python 3
* pip3 

## Usage

Install dependency
```bash
pip install -r requirements.txt
```

Environment variables

| Variable name    | Default value  | Comment                       |
|:-----------------|:---------------|-------------------------------|
| KUBECONFIG       | ~/.kube/config | k8s API client                |
| K8S_NAMESPACES   |  | Namespaces delimited by comma |
| K8S_DELIMETER    | ;              | Result table delimeter        |
| K8S_BEARER_TOKEN |                | Bearer token for API          |
| K8S_CONTEXT      | default        | Context                       |


Run
```bash
K8S_BEARER_TOKEN=token1234 \
KUBECONFIG=C:\somewhere\kube-config \
K8S_NAMESPACES=some-namespace1,somenamespace2 \
kubectl-rescalc.py
```
