from ZillowHouseData.config.configuration import ConfigurationManager
from ZillowHouseData.components.data_ingestion import DataIngestion
from ZillowHouseData.logger import logger
from ZillowHouseData.exception import CustomException
import sys

STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def data_ingestion(self):
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")


    def ingestion_stage(self):
        try:
            obj = DataIngestionTrainingPipeline()
            obj.data_ingestion()
        except Exception as e:
            logger.exception(e)
            raise CustomException(e,sys)