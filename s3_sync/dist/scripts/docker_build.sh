#!/bin/sh

docker build -t karthyuom/k8-s3-sync:1.0 -f ../../Dockerfile ../../

docker push karthyuom/k8-s3-sync:1.0
