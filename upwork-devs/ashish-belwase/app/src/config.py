import os


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        exit(f"{k} not supplied")
    return val


class Config(object):
    DEBUG = True
    glasswall_url = get_envar("glasswall_url")
    virusshare_url = get_envar("virusshare_url")
    virusshare_hash_url = get_envar("virusshare_hash_url")
    virustotal_url = get_envar("virustotal_url")
