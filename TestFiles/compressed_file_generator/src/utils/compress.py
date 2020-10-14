import os
import zipfile
from os.path import basename
import subprocess
import py7zr
import tarfile
import gzip
import shutil
import patoolib

class Compress:
    @staticmethod
    def zip_compresstion(zip_path,zip_filename,file_path ):
        filename = f"{zip_path}{zip_filename}.zip"
        zipfile.ZipFile(filename, mode="w").write(
            file_path, basename(file_path)
        )
        return zip_filename

    @staticmethod
    def seven_z_compresstion(zip_path, zip_filename, file_path ):
        filename = f"{zip_path}{zip_filename}.7z"
        with py7zr.SevenZipFile(filename, 'w') as z:
            z.writeall(file_path,basename(file_path))
        return zip_filename

    @staticmethod
    def tar_compresstion(zip_path,zip_filename,file_path):
        filename= f"{zip_path}{zip_filename}.tar"
        with tarfile.open(filename, "w:gz") as tar_handle:
            tar_handle.add(file_path, arcname=os.path.basename(file_path))
        tar_handle.close()
        return zip_filename

    @staticmethod
    def gz_compresstion(zip_path,zip_filename,file_path):
        filename= f"{zip_path}{zip_filename}.gz"
        with tarfile.open(filename, "w:gz") as tar_handle:
            tar_handle.add(file_path, arcname=os.path.basename(file_path))
        tar_handle.close()
        return zip_filename


    #     with gzip.open(gz_filename, 'wb') as f_out:
    #         with open(file_path, 'rb') as f_in:
    #             shutil.copyfileobj(f_in, f_out)
    #
    #     return gz_filename

    # @staticmethod
    # def rar_compresstion(zip_path, zip_filename, file_path):
    #     rar_filename = f"{zip_path}{zip_filename}.rar"
    #     patoolib.create_archive(rar_filename, file_path)
    #     return rar_filename



