from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.components.model_evaluate import ModelEvaluate
from src.ZillowHouseData.utils.common import load_keras_model, load_pickle_object
from src.ZillowHouseData.config.configuration import ConfigurationManager
import sys

STAGE_NAME = "Model Evaluation"

class ModelEvaluatePipeline:
    def __init__(self):
        pass

    def data_evaluate(self):
        
        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")
        loaded_model = load_keras_model("models", "model.keras")
        logger.info(">>>>>> Loaded saved model successfully<<<<<<\n\nx==========x")

        X_test_scaled = load_pickle_object("models", "X_test_scaled.pkl")
        y_test = load_pickle_object("models", "y_test.pkl")
        logger.info(">>>>>> Loaded X_test and y_test successfully<<<<<<\n\nx==========x")

        # Evaluate model
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluate = ModelEvaluate(config=model_evaluation_config)
        mse = model_evaluate.evaluate_model(loaded_model, X_test_scaled, y_test)
        logger.info(f">>>>>> Model validation completed with MSE {mse} <<<<<<\n\nx==========x")
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj3 = ModelEvaluatePipeline()
        obj3.data_evaluate()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e,sys)