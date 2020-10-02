import requests

class MQService:

    @staticmethod
    def send(payload):
        # Replace this with Viraj's c
    	response = requests.post("http://k8-s3-sync:5004/tos3", json=payload)
    	#print(response.content)
