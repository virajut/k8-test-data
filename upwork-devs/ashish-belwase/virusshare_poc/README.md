# VirusShare POC

### Usage

## Run app

`python main.py`

## Run test cases
`python -m unittest`

### Endpoints

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/scrape-vs-file`  | Download a file from VS   | `{"api_key": "","hash"   : ""}` |
| `/check-malicious` | Check if a file is malicious   | `{"file": "<binary file>"}` |

## Docker Image

### Build

To build the Docker image and name it `k8-test-data` run:

`docker build -t k8-test-data .`

To push
`docker push <username>/k8-test-data`

### Run

To run the aforementioned built image run:

`docker run -p 5000:5000 -it --rm k8-test-data`


## Kubernetes

To run through kubernetes

`kubectl apply -f deploy.yaml`
