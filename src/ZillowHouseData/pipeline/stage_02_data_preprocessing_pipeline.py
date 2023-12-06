from src.ZillowHouseData.components.data_preprocessing import DataPreprocessing
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.config.configuration import ConfigurationManager
from src.ZillowHouseData.pipeline.stage_01_data_ingestion_pipeline import ingestion_stage
import sys

STAGE_NAME = "Data Preprocessing stage"

class DataPreprocessingTrainingPipeline:
    def __init__(self):
        pass

    def data_preprocess(self):
            # Create an instance of the DataPreprocessing class
            logger.info(f">>>>>> stage {STAGE_NAME} initated <<<<<<\n\nx==========x")
            config = ConfigurationManager()
            data_preprocessing_config = config.get_data_preprocessing_config()
            data_preprocessor = DataPreprocessing(config = data_preprocessing_config)

            logger.info(">>>>>> Parsing and Filtering data <<<<<<\n\nx==========x")
            load_df = data_preprocessor.read_and_filter_data()

            logger.info(">>>>>> exact year & month <<<<<<\n\nx==========x")
            filter_df = data_preprocessor.get_year_month(load_df)

            logger.info(">>>>>> get stats <<<<<<\n\nx==========x")
            stats_df = data_preprocessor.get_stats(filter_df)

            logger.info(">>>>>> merging data <<<<<<\n\nx==========x")
            final_data = data_preprocessor.get_merge(stats_df, filter_df)
            
            logger.info(f">>>>>> stage {STAGE_NAME}completed <<<<<<\n\nx==========x")


    def preprocessing_stage(self):
    #ingestion_stage()
        try:
            obj1 = DataPreprocessingTrainingPipeline()
            obj1.data_preprocess()
        except Exception as e:
            logger.exception(e)
            raise CustomException(e,sys)
    
