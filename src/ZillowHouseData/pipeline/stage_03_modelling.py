from src.ZillowHouseData.components.data_model import DataModeling
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.config.configuration import ConfigurationManager
import sys
import os  # Don't forget to import 'os'

STAGE_NAME = "Data Modelling stage"

class DataModellingPipeline:
    def __init__(self):
        pass

    def data_model(self):
        # Create an instance of the Modelling class   
        logger.info(f">>>>>> stage {STAGE_NAME} initiated <<<<<<\n\nx==========x")
        file_path = os.path.join('artifacts', 'data_ingestion', 'final.csv')
        data_modeling = DataModeling(file_path)

        logger.info(f">>>>>> CSV read <<<<<<\n\nx==========x")
        # Read data
        df = data_modeling.read_csv_to_dataframe()

        logger.info(f">>>>>> Test train split <<<<<<\n\nx==========x")

        # Preprocess data
        X_train_scaled, X_test_scaled, y_train, y_test, scaler = data_modeling.preprocess_data(df)

        logger.info(f">>>>>> Build model <<<<<<\n\nx==========x")
        # Build model
        model = data_modeling.build_model(X_train_scaled.shape[1])

        logger.info(f">>>>>> Train model <<<<<<\n\nx==========x")
        # Train model
        model = data_modeling.train_model(model, X_train_scaled, y_train)

        logger.info(f">>>>>> Evaluate model <<<<<<\n\nx==========x")
        # Evaluate model
        mse = data_modeling.evaluate_model(model, X_test_scaled, y_test)

        logger.info(f">>>>>> Prediction <<<<<<\n\nx==========x")
        # Predict on a sample
        data_modeling.predict_sample(model, scaler)

        logger.info(f">>>>>> User prediction <<<<<<\n\nx==========x")
        # Predict using user input
        data_modeling.predict_user_input(model, scaler)

    def modelling_stage(self):
        try:
            obj2 = DataModellingPipeline()
            obj2.data_model()
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)

# Create an instance of DataModellingPipeline
#obj = DataModellingPipeline()

# Call the method processing_stage
#obj.processing_stage()
