from src.ZillowHouseData.components.user_predict import Predict
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.utils.common import load_keras_model, load_pickle_object
from src.ZillowHouseData.config.configuration import ConfigurationManager
import sys

STAGE_NAME = "User Predict"

class UserPredictPipeline:
    def __init__(self):
        pass

    def user_predict(self):
        
        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")

        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")
        loaded_model = load_keras_model("models", "model.keras")
        logger.info(">>>>>> Loaded saved model successfully<<<<<<\n\nx==========x")

        scaler = load_pickle_object("models", "scaler.pkl")
        logger.info(">>>>>> Loaded model and scaler successfully<<<<<<\n\nx==========x")
        

        config = ConfigurationManager()
        user_predict_config = config.get_user_input_predic_config()
        predict_pipeline = Predict(config= user_predict_config)
        predict_pipeline.predict_user_input(loaded_model, scaler)
        logger.info(">>>>>> Prediction pipeline completed <<<<<<\n\nx==========x")

    def evaluation_stage(self):
        try:
            obj4 = UserPredictPipeline()
            obj4.user_predict()
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)