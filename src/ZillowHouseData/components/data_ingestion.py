import os, sys
import zipfile
import gdown
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.entity.config_entity import DataIngestionConfig

# class DataIngestion:
#     def __init__(self, config: DataIngestionConfig):
#         self.config = config

    
#     def download_file(self)-> str:
#         '''
#         Fetch data from the url
#         '''

#         try: 
#             dataset_url = self.config.source_URL
#             zip_download_dir = self.config.local_data_file

#             dir_path = "artifacts/data_ingestion"
#             if not os.path.exists(dir_path):
#                 os.makedirs(dir_path)
#             logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

#             file_id = dataset_url.split("/")[-2]
#             prefix = 'https://drive.google.com/uc?/export=download&id='
#             gdown.download(prefix+file_id,zip_download_dir)

#             logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

#         except Exception as e:
#             raise CustomException(e,sys)
        

#     def extract_zip_file(self):
#         """
#         zip_file_path: str
#         Extracts the zip file into the data directory
#         Function returns None
#         """
#         unzip_path = self.config.unzip_dir
#         os.makedirs(unzip_path, exist_ok=True)
#         with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
#             zip_ref.extractall(unzip_path)
#             logger.info("Extracted parent zip file")
        
#         # Get the path to the current working directory
#         os.chdir(unzip_path)
#         current_working_directory = os.getcwd()

#         # Iterate over the files in the current working directory
#         for file in os.listdir(current_working_directory):
#             # If the file is a zip file, unzip it
#             if file.endswith(".zip"):
#                 with open(os.path.join(current_working_directory, file), 'rb') as f:
#                     zipfile.ZipFile(f).extractall()
#                     logger.info(f"{file} data files extracted successfully")

#         # Deleting zipfiles            
#         for file in os.listdir(current_working_directory):
#             if file.endswith(".zip"):
#                 logger.info(f"Deleted {file} file")
#                 os.remove(file)
        
#         # Reset cwd+
          
#         os.chdir('../..')
#         logger.info(f"working directory resetted to {os.getcwd()}")


import os, sys, json, shutil
import zipfile
import requests

class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        try:
            dataset_list = ["https://data.nasdaq.com/api/v3/datatables/ZILLOW/REGIONS?qopts.export=true&api_key=yaXdjWK7YAbeWZMoqphn", "https://data.nasdaq.com/api/v3/datatables/ZILLOW/INDICATORS?qopts.export=true&api_key=yaXdjWK7YAbeWZMoqphn","https://data.nasdaq.com/api/v3/datatables/ZILLOW/DATA?qopts.export=true&api_key=yaXdjWK7YAbeWZMoqphn"]
            for dataset_url in dataset_list:
                json_download_dir = "artifacts/data_ingestion/json"
                self.json_file_path = os.path.join(json_download_dir, "download_link_indic.json")
                self.zip_download_dir = "artifacts/data_ingestion/zip"
                self.zip_file_path = os.path.join(self.zip_download_dir, "data.zip")

                logger.info("1")
                # Create directories if they don't exist
                if not os.path.exists(json_download_dir):
                    os.makedirs(json_download_dir)
                if not os.path.exists(self.zip_download_dir):
                    os.makedirs(self.zip_download_dir)
                logger.info("2")
                # Download JSON file with download link
                response = requests.get(dataset_url)
                if response.status_code == 200:
                    with open(self.json_file_path, 'wb') as file:
                        file.write(response.content)
                logger.info("3")
                # Read download link from JSON file
                with open(self.json_file_path, 'r') as json_file:
                    download_link = json.loads(json_file.read())["datatable_bulk_download"]["file"]["link"]
                logger.info("4")
                # Download ZIP file
                response = requests.get(download_link)
                if response.status_code == 200:
                    with open(self.zip_file_path, 'wb') as file:
                        file.write(response.content)
                logger.info("5")
                self.extract_zip_file()

        except Exception as e:
            raise e

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        Function returns None
        """
        try:

            unzip_path = "artifacts/data_ingestion"
            if not os.path.exists(unzip_path):
                os.makedirs(unzip_path)

            # unzip_path = self.config.unzip_dir
            os.makedirs(unzip_path, exist_ok=True)

            with zipfile.ZipFile('artifacts/data_ingestion/zip/data.zip', 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
                logger.info("Extracted zip file")
            
            if os.path.isdir(os.path.dirname(self.json_file_path)):
                shutil.rmtree(os.path.dirname(self.json_file_path))

            if os.path.isdir(os.path.dirname(self.zip_file_path)):
                shutil.rmtree(os.path.dirname(self.zip_file_path))

        except Exception as e:
            raise CustomException(e,sys)

        logger.info("Zip file extraction complete")
