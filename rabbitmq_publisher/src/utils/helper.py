import logging

logger = logging.getLogger("GW: RabbitMQ Publisher")

def get_file_extension(file_name):
    if file_name:
        try:
            extension = file_name.split('.')[-1]
            return extension
        except Exception as err:
            logger.error(str(err))
            raise Exception('Invalid filename, mising extension: {0}'.format(str(err)))