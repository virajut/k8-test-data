import os
from flask import Flask, request, jsonify, send_file
import logging as logger

from src.config import Config
from src.services import (
    MinioService,
    FileService,
    VirusTotalService,
    GlasswallService,
    MQService,
)

logger.basicConfig(level=logger.INFO)


class Processor:
    def __init__(self, filename):
        self.filename = filename
        self.directory = None
        self.path = None
        self.minio = MinioService(
            Config.MINIO_URL, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY
        )

    def create_directory(self):
        self.directory = self.filename.split(".")[0]
        self.path = self.directory + "/" + self.filename
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def download_and_unzip(self):
        logger.info(f"downloading file {self.filename} from minio")
        self.minio.download_files("zip", self.filename, self.directory)

        # unzip file
        FileService.unzip(self.path, self.directory)

    def check_malicious(self):
        logger.info("checking malicious with VirusTotal")
        VirusTotalService.check_malicious(self.path)

    def rebuild_glasswall(self):
        logger.info("rebuilding with GW engine")
        GlasswallService.rebuild(self.path)

    def prepare_result(self):
        logger.info("combining all reports, original file and malicious file to a zip")
        FileService.prepare_zip(self.path)

    def upload(self):
        logger.info("uploading to minio")
        FileService.upload(self.path)

    def send_mq(self):
        logger.info("sending file to rabbitmq for s3 sync")
        MQService.send({})

    def process(self):
        logger.info(f"processing {self.filename}")
        default_exceptions = Exception
        processes = [
            (self.create_directory, default_exceptions),
            (self.download_and_unzip, (ValueError, TypeError)),
            (self.check_malicious, default_exceptions),
            (self.rebuild_glasswall, default_exceptions),
            (self.prepare_result, default_exceptions),
            (self.upload, default_exceptions),
            (self.send_mq, default_exceptions),
        ]
        for proc, exceptions in processes:
            try:
                proc()
            except exceptions as e:
                logger.error(f"Error processing file {self.filename} : " + str(e))
                break


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/process", methods=["POST"])
    def get_files():
        data = request.json
        """
        To do process file 
        """
        file = data.get("file", None)
        if not file:
            return jsonify({"message": "No file"})

        Processor(file).process()
        return jsonify({})

    return app
