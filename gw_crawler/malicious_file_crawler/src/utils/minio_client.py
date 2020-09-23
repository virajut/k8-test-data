import logging
import os
import sys

from storage.src.minio_service import MinioService

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

logger = logging.getLogger("GW:minio")


class MinioClient:
    @staticmethod
    def get_client():
        try:
            client = MinioService.get_storage_adapter()
        except Exception:
            raise Exception("client not found")
        else:
            return client
