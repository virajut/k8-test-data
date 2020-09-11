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
### Open Minio UI on http://localhost:9000 or https:127.0.0.1:9000
### Login to UI
- User: minio
- Password: minio123

##Sample code

```
    minioClient = Minio('localhost:9000',
                    access_key='minio',
                    secret_key='minio123',
                    secure=False)
    text='abc'
    bucket = 'mybucket'
    content =BytesIO(bytes(text,'utf8'))
    size=content.getbuffer().nbytes
    key='sample.text'


    # Make a bucket with the make_bucket API call.
    try:
        minioClient.make_bucket("mybucket", location="us-east-1")
    except BucketAlreadyOwnedByYou as err:
       pass
    except BucketAlreadyExists as err:
       pass
    except ResponseError as err:
       raise

    try:
       minioClient.put_object(bucket,key,content,size)
    except ResponseError as err:
       print(err)

    
```

### Deploy and start your app using Kubernate with Minikube:

```

    eval $(minikube docker-env)

    docker build . -t virusshare:latest

    kubectl apply -f deployment.yaml

    kubectl get deployments

    minikube service virusshare

    if above fails/gives error saying terminal needs to open

    kubectl get pods

    kubectl port-forward virusshare-8455d6bff7-srdhp 5000:5000
```
##Refrence link

```
    https://docs.min.io/docs/python-client-api-reference.html

```







