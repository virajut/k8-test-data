import os
import logging as logger

logger.basicConfig(level=logger.INFO)


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        msg = "{0} not supplied".format(k)
        logger.info(msg)
        exit(msg)
    return val


class Config(object):
    path = "/usr/src/app"
    config_path = path + "/CLI/Configs"
    input_path = path + "/rebuild_files/input"
    output_path = path + "/rebuild_files/output/Managed"
