import requests
import logging

logger = logging.getLogger("GW:file_processor")


class GlasswallService:

    @staticmethod
    def get_file(file, filename):
        file = file + "/" + filename
        try:
            return {"file": (filename, open(file, "rb"))}
        except Exception:
            logger.info(f"unable to get file {file}")
            return False

    @staticmethod
    def rebuild(filename, file, mode='1'):
        files = GlasswallService.get_file(file, filename)
        if not files:
            return False
        output = False
        try:
            response = requests.post("http://glasswall-rebuild:5003/process", files=files, data={'mode':mode })
        except Exception as ex:
            logger.info(str(ex))
        else:
            output = response.content
            if '"message": "failed"' in str(output):
                output = False
        return output
