import os, sys
import zipfile
import gdown
from ZillowHouseData.logger import logger
from ZillowHouseData.exception import CustomException
from ZillowHouseData.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
 
    
    def download_file(self)-> str:
                
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")
 
            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix+file_id,zip_download_dir)
 
            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")
 
 
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            logger.info("Extracted parent zip file")
        
        # Get the path to the current working directory
        os.chdir(unzip_path)
        current_working_directory = os.getcwd()
 
        # Iterate over the files in the current working directory
        for file in os.listdir(current_working_directory):
            # If the file is a zip file, unzip it
            if file.endswith(".zip"):
                with open(os.path.join(current_working_directory, file), 'rb') as f:
                    zipfile.ZipFile(f).extractall()
                    logger.info(f"{file} data files extracted successfully")
 
        # Deleting zipfiles            
        for file in os.listdir(current_working_directory):
            if file.endswith(".zip"):
                logger.info(f"Deleted {file} file")
                os.remove(file)
        
        # Reset cwd+
          
        os.chdir('../..')
        logger.info(f"working directory resetted to {os.getcwd()}")