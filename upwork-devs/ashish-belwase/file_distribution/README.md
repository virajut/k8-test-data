# File Distribution Service

### Usage

## Run app

`python main.py`

## Run test cases
`python -m unittest`

### Endpoints [ All POST ]

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/files` | Get malicious files   | `{"file_type": "txt", "num_files":2}` |	

## Docker Image

### Build

To build the Docker image and name it `k8-file-distribution` run:

`docker build -t k8-file-distribution .`

To push
`docker push <username>/k8-file-distribution`

### Run

To run the aforementioned built image run:

`docker run -e PYTHONUNBUFFERED=0 -p 5001:5000 -it --rm k8-file-distribution`

