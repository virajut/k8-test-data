import requests


class GlasswallService:
    @staticmethod
    def rebuild(filename, file, mode='1'):
        file = file + "/" + filename
        files = {"file": (filename, open(file, "rb"))}
        response = requests.post("http://glasswall-rebuild:5003/process", files=files, data={'mode':mode })
        output = response.content
        try:
            if '"message": "failed"' in response:
                output = False
        except:
            pass
        return output
