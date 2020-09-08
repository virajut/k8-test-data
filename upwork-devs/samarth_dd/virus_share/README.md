## Docker Minikube Kubernates Flask App


## Install minikube
```
    brew install minikube
```
## Start minikube
```
    minikube start --driver=virtualbox
```
## Deploy Minio 
```
    git clone https://github.com/minio/operator.git
    cd operator
    kubectl apply -k github.com/minio/operator
    kubectl apply -f https://raw.githubusercontent.com/minio/operator/master/examples/tenant.yaml
    kubectl port-forward service/minio 9000:9000
```
### Open Minio UI on http://localhost:9000
See screenshot ![minio](minio.png)
### Login to UI
- User: minio
- Password: minio123

```bash
docker build . -t virusshare

```

### Minikube:

```bash
eval $(minikube docker-env)

docker build . -t virusshare:latest

kubectl apply -f deployment.yaml

kubectl get deployments


minikube service virusshare

if above fails/gives error saying terminal needs to open

kubectl get pods

kubectl port-forward virusshare-8455d6bff7-srdhp 5000:5000

```
