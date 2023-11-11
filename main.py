import sys
from ZillowHouseData.logger import logger
from ZillowHouseData.exception import CustomException
from ZillowHouseData.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

# # Checking logger and Exception
# # logging
# logger.info("Logging Successfull!!!")

# # exception
# try:
#     a=1/0
# except Exception as e:
#     logger.info("Divide by zero")
#     raise CustomException(e,sys)

STAGE_NAME = "Data Ingestion stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys)

