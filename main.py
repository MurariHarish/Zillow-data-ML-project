import sys
from ZillowHouseData.logger import logger
from ZillowHouseData.exception import CustomException
from ZillowHouseData.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from ZillowHouseData.pipeline.stage_02_data_preprocessing import DataPreprocessingTrainingPipeline
from ZillowHouseData.pipeline.stage_03_modelling import DataModellingPipeline

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
'''
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys) 

STAGE_NAME = "Data Preprocessing Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataPreprocessingTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys)'''

STAGE_NAME = "Data Modelling Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj2 = DataModellingPipeline()
    obj2.processing_stage()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys)

