FROM python:3.6
EXPOSE 50057
ARG MINIO_ENDPOINT
ARG MINIO_ACCESS_KEY_ID
ARG MINIO_SECRET_ACCESS_KEY
ARG MINIO_SECURE
ARG MQ_USERNAME
ARG MQ_PASSWORD
ARG MQ_HOST
ARG MQ_PORT
ARG MQ_QUEUE
ARG MQ_ROUTING_KEY
ARG s3_sync_api
ARG file_processor_api

WORKDIR /usr/src/app
COPY rabbitmq/requirements.txt .
RUN pip install -r requirements.txt
COPY rabbitmq .
CMD [ "python", "main.py" ]
