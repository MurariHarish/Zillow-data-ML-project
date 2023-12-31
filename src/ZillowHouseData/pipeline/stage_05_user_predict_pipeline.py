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

    def user_predict(self, user_input):
        
        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")

        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")
        loaded_model = load_keras_model("models", "model.keras")
        logger.info(">>>>>> Loaded saved model successfully<<<<<<\n\nx==========x")

        scaler = load_pickle_object("models", "scaler.pkl")
        logger.info(">>>>>> Loaded model and scaler successfully<<<<<<\n\nx==========x")
        

        config = ConfigurationManager()
        user_predict_config = config.get_user_input_predic_config()
        predict_pipeline = Predict(config= user_predict_config)
        pred_value = predict_pipeline.predict_user_input(loaded_model, scaler, user_input)
        logger.info(">>>>>> Prediction pipeline completed <<<<<<\n\nx==========x")
        return pred_value
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj4 = UserPredictPipeline()
        obj4.user_predict()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e,sys)