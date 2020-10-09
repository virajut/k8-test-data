import logging as logger
import os
import zipfile
from os.path import basename
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
    def __init__(self, filename, bucket_name):
        self.filename = filename
        self.bucket_name = bucket_name
        self.hash = self.filename.split(".")[0]
        self.ext = None
        self.directory = None
        self.path = None
        self.infected_path = None
        self.infected_file = filename
        self.virus_total_status = False
        self.gw_rebuild_status = False
        self.minio = MinioService(
            Config.MINIO_URL, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY
        )
        self.vt = VirusTotalService(Config.virustotal_key)

    def create_directory(self):
        try:
            self.directory = Config.download_path + "/" + self.filename.split(".")[0]
            self.infected_path = self.directory + "/infected"
            self.path = self.directory + "/" + self.filename
            Path(self.infected_path).mkdir(parents=True, exist_ok=True)
        except Exception as error:
            logger.error(f'Processor : create_directory error: {error}')
            raise error

    def download_and_unzip(self):
        try:
            logger.info(f"downloading file {self.filename} from minio")
            self.ext = self.filename.split(".")[-1]
            download_path = self.directory if self.ext == "zip" else self.infected_path

            self.minio.download_files(bucket_name=self.ext, file_name=self.filename, download_path=download_path)

            if self.ext == "zip":
                FileService.unzip(self.path, self.infected_path)
                file = os.listdir(self.infected_path)
                if not file:
                    logger.error("no file inside zip")
                else:
                    base_path = self.infected_path + "/"
                    os.rename(base_path + file[0], base_path + self.hash + "." + file[0].split(".")[-1])
                    self.infected_file = file[0]
        except Exception as error:
            logger.error(f'Processor : download_and_unzip error: {error}')
            raise error


        except Exception as error:
            logger.error(f'Processor : download_and_unzip error: {error}')
            raise error

    def check_virustotal(self):
        try:
            logger.info("checking malicious with VirusTotal")

            resp = self.vt.file_scan(self.infected_path + "/" + self.infected_file)
            logger.info(f"Processor : check_virustotal report status: {resp['status_code']}")
            if resp['status_code'] == 200:
                self.virus_total_status = True
                vt_file_name = self.directory + '/virustotal_' + self.hash + '.json'

                with open(vt_file_name, "w") as fp:
                    fp.write(str(resp))

        except Exception as e:
            logger.error(f'Processor : check_virustotal error: {e}')
            raise e

    def get_metadata(self):
        logger.info("getting metadata of the file")
        try:
            self.metadata = FileService.get_file_meta(self.infected_path + "/" + self.infected_file)
            meta = self.metadata
            meta['url'] = None
            if meta:
                minio_meta = self.minio.get_stat(bucket_name=self.bucket_name, file_name=self.filename)

                logger.info(f'minio_meta {minio_meta}')
                if 'x-amz-meta-url' in minio_meta.metadata:
                    meta['url'] = minio_meta.metadata['x-amz-meta-url']
                meta['virus_total_status'] = self.virus_total_status
                meta['gw_rebuild_status'] = self.gw_rebuild_status

            meta_file_name = self.directory + '/metadata_' + self.hash + ".json"

            with open(meta_file_name, "w") as fp:
                fp.write(str(meta))
        except Exception as e:
            logger.error(f'Processor : get_metadata error: {e}')
            raise e

    def rebuild_glasswall(self):
        logger.info("rebuilding with GW engine")
        try:
            response = GlasswallService.rebuild(self.infected_file, self.infected_path)
            file = response.content
            status = response.status_code
            logger.info(f'Processor : rebuild_glasswall report status: {status}')

            if status == 200:
                self.gw_rebuild_status = True
                with open(self.directory + f"/rebuild_{self.infected_file}", "wb") as fp:
                    fp.write(file)

        except Exception as e:
            logger.error(f'Processor : rebuild_glasswall error: {e}')
            raise e

    def prepare_result(self):
        try:
            logger.info("combining all reports, original file and malicious file to a zip")
            file_path = self.infected_path + "/" + self.infected_file
            malware_zip_name = self.directory + '/' + self.directory.split("/")[-1] + '.zip'

            zipfile.ZipFile(malware_zip_name, mode='w').write(file_path, basename(file_path))
            os.remove(self.infected_path + "/" + self.infected_file)

            FileService.prepare_zip(
                zip_filename=self.directory.split("/")[-1],
                folder_path=self.directory,
                zip_path=Config.download_path
            )

        except Exception as error:
            logger.error(f'Processor : prepare_result: {error}')
            raise error

    def upload(self):
        try:
            logger.info("uploading to minio")
            name = self.directory.split("/")[-1]
            self.minio.upload(
                file_path=Config.download_path + "/" + name + ".zip",
                bucket_name="processed",
                file_name=name + ".zip"
            )
        except Exception as error:
            logger.error(f'Processor : upload error: {error}')
            raise error

    def send_mq(self):
        try:
            logger.info("sending file to rabbitmq for s3 sync")
            name = self.directory.split("/")[-1]
            payload = {
                's3_bucket': self.ext,
                'minio_bucket': "processed",
                'file': name + ".zip"
            }
            MQService.send(payload)
        except Exception as error:
            logger.error(f'Processor : send_mq: {error}')
            raise error

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
        bucket_name = data.get("bucket", None)
        if not file:
            return jsonify({"message": "No file"})

        Processor(file, bucket_name).process()
        return jsonify({})

    return app
