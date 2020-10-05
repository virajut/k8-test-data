import logging as logger
import os
from pathlib import Path
from flask import Flask, request, jsonify
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
        self.ext = None
        self.directory = None
        self.path = None
        self.infected_path = None
        self.infected_file = filename
        self.minio = MinioService(
            Config.MINIO_URL, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY
        )
        self.vt = VirusTotalService(Config.virustotal_key)

    def create_directory(self):
        self.directory = Config.download_path + "/" + self.filename.split(".")[0]
        self.infected_path = self.directory + "/infected"
        self.path = self.directory + "/" + self.filename
        Path(self.infected_path).mkdir(parents=True, exist_ok=True)

    def download_and_unzip(self):
        logger.info(f"downloading file {self.filename} from minio")
        self.ext = self.filename.split(".")[-1]
        download_path = self.directory if self.ext == "zip" else self.infected_path
        self.minio.download_files(self.ext, self.filename, download_path)

        if self.ext == "zip":
            FileService.unzip(self.path, self.infected_path)
            file = os.listdir(self.infected_path)
            if not file:
                logger.error("no file inside zip")
            self.infected_file = file[0]

    def check_virustotal(self):
        logger.info("checking malicious with VirusTotal")
        # print(self.infected_path + "/" + self.infected_file)
        resp = self.vt.file_scan(self.infected_path + "/" + self.infected_file)
        # resp = "{'test':'1'}"
        with open(self.directory + "/virustotal.json", "w") as fp:
            fp.write(str(resp))

    def get_metadata(self):
        logger.info("getting metadata of the file")
        self.metadata = FileService.get_file_meta(self.infected_path + "/" + self.infected_file)
        meta = self.metadata

        with open(self.directory + "/"+ meta['hash']+ ".json", "w") as fp:
            fp.write(str(meta))

    def rebuild_glasswall(self):
        logger.info("rebuilding with GW engine")
        file = GlasswallService.rebuild(self.infected_file, self.infected_path)
        if file:
            with open(self.directory + f"/rebuild_{self.infected_file}", "wb") as fp:
                fp.write(file)

    def prepare_result(self):
        logger.info("combining all reports, original file and malicious file to a zip")
        FileService.prepare_zip(
            self.directory.split("/")[-1], self.directory, Config.download_path
        )

    def upload(self):
        logger.info("uploading to minio")
        name = self.directory.split("/")[-1]
        self.minio.upload(
            Config.download_path + "/" + name + ".zip", "processed", name + ".zip"
        )

    def send_mq(self):
        logger.info("sending file to rabbitmq for s3 sync")
        name = self.directory.split("/")[-1]
        payload = {
            's3_bucket': self.ext,
            'minio_bucket': "processed",
            'file': name + ".zip"
        }
        MQService.send(payload)

    def process(self):
        logger.info(f"processing {self.filename}")
        default_exceptions = Exception
        processes = [
            (self.create_directory, default_exceptions),
            (self.download_and_unzip, (ValueError, TypeError)),
            (self.check_virustotal, default_exceptions),
            (self.rebuild_glasswall, default_exceptions),
            (self.get_metadata, default_exceptions),
            (self.prepare_result, default_exceptions),
            (self.upload, default_exceptions),
            (self.send_mq, default_exceptions),
        ]
        for proc, exceptions in processes:
            try:
                proc()
            except exceptions as e:
                logger.error(f"Error processing file {self.infected_file} : " + str(e))
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
