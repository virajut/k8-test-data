#!/bin/sh

docker build -t karthyuom/glasswall-rebuild -f ../../Dockerfile ../../

docker push karthyuom/glasswall-rebuild
