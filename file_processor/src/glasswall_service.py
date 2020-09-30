import requests


class GlasswallService:
    @staticmethod
    def rebuild(filename, file):
        files = {"file": (filename, open(file + "/" + filename, "rb"))}
        response = requests.post("http://glasswall-rebuild:5003/process", files=files)
        return response.content
