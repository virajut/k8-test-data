# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import os

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.misc import md5sum
from six import BytesIO

from .utils.bundle_zip import BundleZip

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MaliciousFileCrawlerPipeline(FilesPipeline):

    def file_downloaded(self, response, request, info, unzip_path=None):
        path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)

        if (response.status == 200):

            if (info.spider.name == "virusshare"):
                file_name = response.headers["Content-Disposition"].split(b'filename=')[1].decode("utf-8")
                path = FilesPipeline.MEDIA_NAME + "/" + file_name
            checksum = md5sum(buf)
            buf.seek(0)
            self.store.persist_file(path, buf, info)

            spider_name = info.spider.name

            try:
                BundleZip.process_malware(path, spider_name)
            except:
                raise Exception("Error while bundle zip")
            return checksum
