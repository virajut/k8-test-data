import os
import glob


class Utils:
    @staticmethod
    def truncate_folder(folder):
        files = glob.glob(folder + "/*")
        for f in files:
            os.remove(f)
