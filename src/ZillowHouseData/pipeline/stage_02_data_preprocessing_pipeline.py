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
            data_preprocessor = DataPreprocessing()
            # Replace 'your_data_bytes_here' with the actual data bytes you want to process
            #data = b'your_data_bytes_here'
            # Stage 1: Data Preprocessing
            load_df = data_preprocessor.read_and_filter_data()
            # Stage 2: Extract Year and Month
            logger.info(f">>>>>> exact year & month <<<<<<\n\nx==========x")
            filter_df = data_preprocessor.get_year_month(load_df)
            # Stage 3: Get Stats
            logger.info(f">>>>>> get stats <<<<<<\n\nx==========x")
            stats_df = data_preprocessor.get_stats(filter_df)
            # print(processed_data.head())
            # Stage 4: Merge Data
            logger.info(f">>>>>> merging data <<<<<<\n\nx==========x")
            final_data = data_preprocessor.get_merge(stats_df, filter_df)
            # print(final_data.head())
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")


    def preprocessing_stage(self):
    #ingestion_stage()
        try:
            obj1 = DataPreprocessingTrainingPipeline()
            obj1.data_preprocess()
        except Exception as e:
            logger.exception(e)
            raise CustomException(e,sys)
    
