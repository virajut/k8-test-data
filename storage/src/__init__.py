import json
import os
import socket

from .minio_service import MinioService



from flask import Flask, request,Response

from .config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)



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
    def upload():
        try:
            client=MinioService(endpoint=os.environ['MINIO_HOSTNAME'], access_key=os.environ['MINIO_ACCESS_KEY_ID'],
                         secret_key=os.environ['MINIO_SECRET_ACCESS_KEY'], secure=False)
            content=request.json
            client.upload_file(content['bucket_name'], content['minio_path'], content['file'])
            ret = {"err": "none", 'details':content}
        except Exception as error:
            ret = {"err": "none", "details": error}
            raise error

        return Response(json.dumps(ret), mimetype='application/json')

    return app








