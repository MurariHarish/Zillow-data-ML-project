from src.ZillowHouseData.components.model_training import DataModeling
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.utils.common import save_model_to_keras, save_object_to_pickle
from src.ZillowHouseData.utils import common
from src.ZillowHouseData.config.configuration import ConfigurationManager
from src.ZillowHouseData.components.model_evaluate import ModelEvaluate
import os, sys

STAGE_NAME = "Data Modelling"
class DataModellingPipeline:
    def __init__(self):
        pass

    def data_model(self):
        # Create an instance of the Modelling class   
        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")
        file_path = os.path.join('artifacts', 'data_ingestion', 'final.csv')
        data_modeling = DataModeling(file_path)

        # Read data
        df = data_modeling.read_csv_to_dataframe()
        logger.info(">>>>>> CSV read <<<<<<\n\nx==========x")

        logger.info(f">>>>>> Preparing data fror training <<<<<<\n\nx==========x")
        # Preprocess data
        X, y = data_modeling.prepare_data(df)

        #Train test Split
        X_train_scaled, X_test_scaled, y_train, y_test, scaler = data_modeling.train_test_split(X, y)
        logger.info(">>>>>> Test train split completed <<<<<<\n\nx==========x")

        save_object_to_pickle( X_test_scaled, "models", "X_test_scaled.pkl")
        save_object_to_pickle( y_test, "models", "y_test.pkl")
        save_object_to_pickle(scaler, "models", "scaler.pkl")
        logger.info(">>>>>> Saved X_test and y_test as pickle for model evaluation <<<<<<\n\nx==========x")

        # # Build model
        model = data_modeling.build_model(X_train_scaled.shape[1])
        logger.info(">>>>>> Model building completed<<<<<<\n\nx==========x")

        save_model_to_keras(model, "models", "model.keras")
        logger.info(">>>>>> Saved model as pickle <<<<<<\n\nx==========x")

        logger.info(">>>>>> Train model <<<<<<\n\nx==========x")
        model = data_modeling.train_model(model, X_train_scaled, y_train)
        logger.info(">>>>>> Model training completed<<<<<<\n\nx==========x")

        # logger.info(f">>>>>> Evaluate model <<<<<<\n\nx==========x")
        # # Evaluate model
        # mse = data_modeling.evaluate_model(model, X_test_scaled, y_test)

        # logger.info(f">>>>>> Prediction <<<<<<\n\nx==========x")
        # # Predict on a sample
        # data_modeling.predict_sample(model, scaler)

        # logger.info(f">>>>>> User prediction <<<<<<\n\nx==========x")
        # # Predict using user input
        # data_modeling.predict_user_input(model, scaler)

    def modelling_stage(self):
        try:
            obj2 = DataModellingPipeline()
            obj2.data_model()
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)
