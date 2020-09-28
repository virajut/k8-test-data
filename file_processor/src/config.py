import os
import logging

logger = logging.getLogger("GW:file_processor")


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        msg = f"{k} not supplied"
        logger.info(msg)
        exit(msg)
    return val


class Config(object):
    download_path = "/usr/src/app"
