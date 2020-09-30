""" Utility class for reading config from config.ini file """

import configparser
import logging

from src import settings

logger = logging.getLogger(__name__)


# utility class to read properties from config.ini file
class ConfigReader:
    def __init__(self, property_name):
        self.property_name = property_name

    def read_config(self):
        """
                reads configaration from config.ini
        """
        try:
            config = configparser.ConfigParser()
            config.read(settings.CONFIG_FILE)
            config_ref = config[self.property_name]
            return config_ref
        except Exception as e:
            logger.error(f'ConfigReader:read_config:{e}')
            raise FileNotFoundError(e)
