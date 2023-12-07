import sys
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.pipeline.stage_01_data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.ZillowHouseData.pipeline.stage_02_data_preprocessing_pipeline import DataPreprocessingTrainingPipeline
from src.ZillowHouseData.pipeline.stage_03_model_training_pipeline import DataModellingPipeline
from src.ZillowHouseData.pipeline.stage_04_model_evaluate_pipeline import ModelEvaluatePipeline
from src.ZillowHouseData.pipeline.stage_05_user_predict_pipeline import UserPredictPipeline

# # Checking logger and Exception
# # logging
# logger.info("Logging Successfull!!!")

# # exception
# try:
#     a=1/0
# except Exception as e:
#     logger.info("Divide by zero")
#     raise CustomException(e,sys)

STAGE_NAME = "Data Ingestion"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.data_ingestion()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys) 


STAGE_NAME = "Data Preprocessing "

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    obj = DataPreprocessingTrainingPipeline()
    obj.data_preprocess()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys)


STAGE_NAME = "Data Modelling"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    obj2 = DataModellingPipeline()
    obj2.data_model()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys)

STAGE_NAME = "Model Evaluation"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    obj3 = ModelEvaluatePipeline()
    obj3.data_evaluate()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e,sys)

# STAGE_NAME = "User Prediction"

# try:
#     logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
#     obj4 = UserPredictPipeline()
#     obj4.user_predict()
#     logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#     logger.exception(e)
#     raise CustomException(e,sys)

# #-----------------------------------------------------------------------------------------