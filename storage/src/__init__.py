import ast
import json
import logging
import os
import socket
from io import BytesIO

import requests
from flask import Flask, request, Response

from .config import Config
from .minio_service import MinioService

logger = logging.getLogger('GW:Storage')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    client = MinioService(endpoint=os.environ['MINIO_HOSTNAME'], access_key=os.environ['MINIO_ACCESS_KEY_ID'],
                          secret_key=os.environ['MINIO_SECRET_ACCESS_KEY'], secure=False)

    def server_info():
        return {"hostname": socket.gethostname()}

    @app.route("/ping", methods=["GET"])
    def ping():
        data = server_info()
        try:
            data['error']: None
            data["action"] = "pong"
        except Exception as error:
            data['error']: error
            data["action"] = "error"
            raise error
        return Response(json.dumps(data), mimetype='application/json')

    @app.route("/upload", methods=['GET', 'POST'])
    def upload_file():
        try:

            content = request.json
            client.upload_file(bucket_name=content['bucket_name'], file_name=content['minio_path'],
                               file_path=content['file'])
            ret = {"err": "none", 'details': content}
        except Exception as error:
            ret = {"err": "none", "details": error}
            raise error

        return Response(json.dumps(ret), mimetype='application/json')

    @app.route("/upload_stream", methods=['GET', 'POST'])
    def upload_stream():
        try:
            logger.info(f'file name : {request.args.get("name")}')

            bucket = request.args.get('bucket_name')
            name = request.args.get('name')
            length = request.args.get('length')
            metadata = request.args.get('metadata')
            meta = ast.literal_eval(metadata)
            data = BytesIO(request.data)

            client.upload_data_stream(bucket_name=bucket, file_name=name, data_stream=data,
                                      length=data.getbuffer().nbytes, metadata=meta)

            try:
                rabbit_mq_api = os.environ.get('rabbit_mq_api', None)
                logger.info(f"calling rabbit_mq_api {rabbit_mq_api}")

                payload = {'file_name': name, 'bucket_name': bucket}
                payload = json.dumps(payload)
                payload = json.loads(payload)

                logger.info(type(payload))
                logger.info(f"calling payload {payload}")
                response = requests.post(rabbit_mq_api, json=payload)
                logger.info(f"calling response {response}")
            except Exception as ex:
                logger.error(ex)

            ret = {"err": "none"}
        except Exception as error:
            logger.error(f'create_app : upload_stream : {error}')
            ret = {"err": "none"}
            raise error

        return Response(json.dumps(ret), mimetype='application/json')

    return app
