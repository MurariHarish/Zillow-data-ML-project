from ZillowHouseData.components.data_preprocessing import DataPreprocessing
from ZillowHouseData.logger import logger
from ZillowHouseData.exception import CustomException
from ZillowHouseData.config.configuration import ConfigurationManager
from ZillowHouseData.pipeline.stage_01_data_ingestion import ingestion_stage
import sys

STAGE_NAME = "Data Preprocessing stage"

class DataPreprocessingTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
            # Create an instance of the DataPreprocessing class
            logger.info(f">>>>>> stage {STAGE_NAME} initated <<<<<<\n\nx==========x")
            data_preprocessor = DataPreprocessing()
            # Replace 'your_data_bytes_here' with the actual data bytes you want to process
            #data = b'your_data_bytes_here'
            # Stage 1: Data Preprocessing
            processed_data = data_preprocessor.data_preprocessing()
            # Stage 2: Extract Year and Month
            logger.info(f">>>>>> exact year & month <<<<<<\n\nx==========x")
            processed_data = data_preprocessor.get_year_month(processed_data)
            # Stage 3: Get Stats
            logger.info(f">>>>>> get stats <<<<<<\n\nx==========x")
            processed_data = data_preprocessor.get_stats(processed_data)
            # Stage 4: Merge Data
            logger.info(f">>>>>> merging data <<<<<<\n\nx==========x")
            final_data = data_preprocessor.get_merge(processed_data)
            #print(final_data.head())
            logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")



if __name__ == '__main__':
    #ingestion_stage()
    try:
        obj1 = DataPreprocessingTrainingPipeline()
        obj1.main()
    except Exception as e:
        logger.exception(e)
        raise CustomException(e,sys)
    
