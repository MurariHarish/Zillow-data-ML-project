import sys
from src.ZillowHouseData.components.data_preprocessing import DataPreprocessing
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.config.configuration import ConfigurationManager
from src.ZillowHouseData.utils.common import save_object_to_pickle


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

            logger.info(">>>>>> extract year & month <<<<<<\n\nx==========x")
            filter_df = data_preprocessor.get_year_month(load_df)
            filter_df.to_csv('artifacts/data_ingestion/filter_df.csv')
            logger.info(">>>>>> get stats <<<<<<\n\nx==========x")
            stats_df = data_preprocessor.get_stats(filter_df)

            logger.info(">>>>>> merging data <<<<<<\n\nx==========x")
            final_data = data_preprocessor.get_merge(stats_df, filter_df)

            logger.info(f">>>>>> final_data.head(5) <<<<<<\n\nx==========x")
            logger.info(final_data.head(5))


            region_id_region_dict = data_preprocessor.extract_unique_regions(final_data)
            save_object_to_pickle(region_id_region_dict, "models", "region_label")

            logger.info(f">>>>>> stage {STAGE_NAME}completed <<<<<<\n\nx==========x")
    
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj1 = DataPreprocessingTrainingPipeline()
        obj1.data_preprocess()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e,sys)