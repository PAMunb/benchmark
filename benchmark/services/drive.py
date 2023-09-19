"""
this module contains the logic of the drive service
"""
import os
import zipfile
import shutil
import gdown

from benchmark.config import Config

ZIP_FILENAME = "Inputs.zip"


class DriveService:

    def __init__(self) -> None:
        self._config = Config()

    def download_contracts(self):
        """
        downloads contract from google drive
        """
        contracts_download_folder = self._config.contracts_download_folder
        if not os.path.exists(contracts_download_folder):
            os.makedirs(contracts_download_folder)
        else:
            shutil.rmtree(contracts_download_folder, ignore_errors=True)
            os.makedirs(contracts_download_folder)

        inputs_path = os.path.join(contracts_download_folder, ZIP_FILENAME)
        if os.path.exists(inputs_path):
            os.remove(inputs_path)

        gdown.download(
            url=self._config.contracts_zip_url,
            output=inputs_path,
            quiet=True,
            fuzzy=True,
        )

        with zipfile.ZipFile(inputs_path, 'r') as zip_file:
            zip_file.extractall(contracts_download_folder)

        os.remove(inputs_path)
