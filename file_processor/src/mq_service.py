import os

import requests

class MQService:

    @staticmethod
    def send(payload):
        s3_sync_api=os.environ.get('s3_sync_api')
        response = requests.post(s3_sync_api, json=payload)

