# Compressed File Generator

## Usage
* Set .env variables from .env.sample

* source_type=minio --> if source/malware files present in minio

* source_type=s3 --> if source/malware files present in minio

## Build

    `To build the Docker image and name it `compressed-file-generator` 

    `docker build -t compressed-file-generator .`


##To run

    `docker run --env-file .env compressed-file-generator`

