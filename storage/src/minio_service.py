import logging
import os
import sys

from .minio_adapter import MinioAdapter

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

logging.basicConfig(filename="testdata_storage.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class MinioService(MinioAdapter):
    def __init__(self, endpoint, access_key, secret_key, secure=False, *args, **kwargs):
        super().__init__(endpoint, access_key, secret_key, secure, *args, **kwargs)