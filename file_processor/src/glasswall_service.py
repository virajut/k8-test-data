import requests


class GlasswallService:
    @staticmethod
    def rebuild(filename, file):
        file = file + "/" + filename
        files = {"file": (filename, open(file, "rb"))}
        response = requests.post("http://glasswall-rebuild:5003/process", files=files)
        output = response
        try:
            if "failed" in response:
                output = False
        except:
            pass
        return output
