#!/bin/sh

docker build -t karthyuom/k8-file-processor:1.0.21 -f ../../Dockerfile ../../

docker push karthyuom/k8-file-processor:1.0.21
