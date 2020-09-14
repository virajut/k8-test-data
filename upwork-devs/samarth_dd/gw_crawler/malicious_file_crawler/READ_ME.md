docker build -t glasswallcrawler:1.0 .

kubectl apply -f minio_service.yaml

kubectl apply -f deployment.yaml

docker-compose up -d

docker run --env-file .env glasswallcrawler:1.0
