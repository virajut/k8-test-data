import logging
import os
import sys

sys.path.append(os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ))
)

from storage.src.minio_service import MinioService

logger = logging.getLogger("GW:minio")


class MinioClient:
    """
            It calls storage adapter to get minio client
    """

    @staticmethod
    def get_client():
        try:
            # client = MinioService.get_storage_adapter()
            endpoint = os.environ["MINIO_URL"]
            access_key = os.environ["MINIO_ACCESS_KEY"]
            secret_key = os.environ["MINIO_SECRET_KEY"]
            secure = False
            client = MinioService(endpoint, access_key, secret_key, secure)

        except Exception:
            logger.error('MinioClient:get_client: Error while gettng client')
            raise Exception("client not found")
        else:
            return client
