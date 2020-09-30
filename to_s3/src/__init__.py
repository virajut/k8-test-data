import os
from flask import Flask, request, jsonify

from src.config import Config
from src.utils.minio_client import MinioClient
from src.utils.s3_client import S3Client

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/tos3", methods=["POST"])
    def sync_to_s3():
        file_to_fetch = request.json() # request should contain minio bucket name, file_name and file to upload
        
        if not "bucket_name" in file_to_fetch:
            return jsonify({"success": False, "error": "bucket_name is missing!"}), 400 

        if not "file_name" in file_to_fetch:
            return jsonify({"success": False, "error": "file name is missing!"}), 400
        
        if not "file" in file_to_fetch:
            return jsonify({"success": False, "error": "file is missing!"}), 400

        minio_client = MinioClient()
        try:
            file_from_minio = minio_client.fetch_file(bucket_name=file_to_fetch['bucket_name'], object_name=file_to_fetch['file_name'], file_path=Config.download_path)
        except Exception as err:
            return jsonify({"success": "False", "error": str(err)}), 400

        s3_client = S3Client()
        try:
            s3_client.upload_file(bucket_name=file_to_fetch['bucket_name'], file_name=file_from_minio)
        except Exception as err:
            return jsonify({"success": "False", "error": str(err)}), 400

        return jsonify({"success": True, "error": None}), 200

    return app
