from datetime import datetime
from src.ZillowHouseData.constants import *
from src.ZillowHouseData.utils.common import create_directories, read_yaml
from src.ZillowHouseData.entity.config_entity import DataIngestionConfig
from src.ZillowHouseData.entity.config_entity import DataPreprocessingConfig
from src.ZillowHouseData.entity.config_entity import ModelTrainingConfig
from src.ZillowHouseData.entity.config_entity import UserPredictConfig

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )
        return data_ingestion_config
    
    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:

        config = self.config.data_preprocessing
        # start_dates = datetime.strptime(self.params.START_DATE, '%Y-%m-%d').date()

        data_preprocessing_config = DataPreprocessingConfig(
            stats_path=Path(config.stats_path),
            final_csv_path=Path(config.final_csv_path),
            file_name=config.file_name,
            start_date=config.start_date,
            interested_columns=config.interested_columns,
            interested_indicators_stats=config.interested_indicators_stats,
            interested_indicators_zhvi=config.interested_indicators_zhvi

        )
        return data_preprocessing_config
    

    def get_model_training_config(self) -> ModelTrainingConfig:

        config = self.config.model_training

        model_training_config = ModelTrainingConfig(
            learning_rate=self.params.LEARNING_RATE,
            epochs=self.params.EPOCHS,
            batch_size=self.params.BATCH_SIZE,
            validation_split=self.params.VALIDATION_SPLIT,
            verbose=self.params.VERBOSE,
            final_csv_path=Path(config.final_csv_path)
        )
        return model_training_config
    
    def get_user_input_predic_config(self) -> UserPredictConfig:
        config = self.config.user_predict

        user_predict_config = UserPredictConfig(
            user_input_reqs=config.user_input_reqs
        )
        return user_predict_config