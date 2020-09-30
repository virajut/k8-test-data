import os
from flask import Flask, request, jsonify

from src.config import Config
from src.utils.minio_client import MinioClient 

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/tos3", methods=["POST"])
    def sync_to_s3():
        file_to_fetch = request.json() # request should contain minio bucket name, file to upload
        


        """
        1. Fetch file from minIO as per request
        2. Put it to S3
        """

    return app
