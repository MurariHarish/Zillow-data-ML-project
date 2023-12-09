import os, sys
from src.ZillowHouseData.components.model_training import DataModeling
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.utils.common import save_model_to_keras, save_object_to_pickle, read_csv_to_dataframe, prepare_data, train_and_test_split
from src.ZillowHouseData.utils import common
from src.ZillowHouseData.config.configuration import ConfigurationManager


STAGE_NAME = "Data Modelling"
class DataModellingPipeline:

    def __init__(self):
        pass

    def data_model(self):
        # Create an instance of the Modelling class   
        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")
        file_path = os.path.join('artifacts', 'data_ingestion', 'final.csv')

        # Read data
        df = read_csv_to_dataframe(file_path)
        logger.info(">>>>>> CSV read <<<<<<\n\nx==========x")

        logger.info(f">>>>>> Preparing data fror training <<<<<<\n\nx==========x")
        # Preprocess data
        X, y, label_to_category_mapping = prepare_data(df)
        save_object_to_pickle(label_to_category_mapping, "models", "label")

        #Train test Split
        X_train_scaled, X_test_scaled, y_train, y_test, scaler = train_and_test_split(X, y)
        logger.info(">>>>>> Test train split completed <<<<<<\n\nx==========x")

        save_object_to_pickle( X_test_scaled, "models", "X_test_scaled.pkl")
        save_object_to_pickle( y_test, "models", "y_test.pkl")
        save_object_to_pickle(scaler, "models", "scaler.pkl")
        logger.info(">>>>>> Saved X_test and y_test as pickle for model evaluation <<<<<<\n\nx==========x")


        config = ConfigurationManager()
        model_training_config = config.get_model_training_config()
        data_modeling = DataModeling(config = model_training_config)

        # Build model
        model = data_modeling.build_model(X_train_scaled.shape[1])
        logger.info(">>>>>> Model building completed<<<<<<\n\nx==========x")

        logger.info(">>>>>> Train model <<<<<<\n\nx==========x")
        model = data_modeling.train_model(model, X_train_scaled, y_train)
        logger.info(">>>>>> Model training completed<<<<<<\n\nx==========x")

        logger.info(">>>>>> model details for me to see : <<<<<<\n\nx==========x")
        model_details = model.summary()
        logger.info(">>>>>> Model Summary <<<<<<\n\nx==========x")
        logger.info(model_details)

        save_model_to_keras(model, "models", "model.keras")
        logger.info(">>>>>> Saved model as pickle <<<<<<\n\nx==========x")


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj2 = DataModellingPipeline()
        obj2.data_model()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e,sys)