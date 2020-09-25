import logging
import os

from src.virus_total import Virustotal

logger = logging.getLogger(__name__)


class MaliciousCheck:

    @staticmethod
    def check_malicious(file_path):
        """
            check_malicious : use VirusTotal api https://www.virustotal.com/vtapi/v2/ to check whether file has malware or not
        """
        try:
            vt = Virustotal(os.environ["VIRUS_TOTAL_KEY"])
            response = vt.file_scan(file_path)
            report = vt.file_report([response['json_resp']['resource']])
        except KeyError:
            logger.error('Invalid configaration for VIRUS_TOTAL_KEY,Configure VIRUS_TOTAL_KEY in .env file ')
            raise ("Invalid configaration for VIRUS_TOTAL_KEY,Configure VIRUS_TOTAL_KEY in .env file ")
        except Exception as error:
            logger.error(f"MaliciousCheck:check_malicious: {error}")
            raise error
        else:
            return report
