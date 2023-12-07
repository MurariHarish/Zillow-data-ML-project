
import sys
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.ZillowHouseData.pipeline.stage_01_data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.ZillowHouseData.pipeline.stage_02_data_preprocessing_pipeline import DataPreprocessingTrainingPipeline
from src.ZillowHouseData.pipeline.stage_03_model_training_pipeline import DataModellingPipeline
from src.ZillowHouseData.pipeline.stage_04_model_evaluate_pipeline import ModelEvaluatePipeline
from src.ZillowHouseData.pipeline.stage_05_user_predict_pipeline import UserPredictPipeline
 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
 
dag = DAG(
    'zillow_data_pipeline',
    default_args=default_args,
    description='Zillow Data Pipeline',
    schedule_interval='@daily',
)
 
def run_stage(stage_name, pipeline_obj, function_name, **kwargs):
    try:
        logger.info(f">>>>>> Stage {stage_name} started <<<<<<")
        obj = pipeline_obj()
        # Invoke the function dynamically using getattr
        getattr(obj, function_name)()
        logger.info(f">>>>>> Stage {stage_name} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e, sys)
 
# DAG for Data Ingestion
data_ingestion_task = PythonOperator(
    task_id='data_ingestion',
    python_callable=run_stage,
    op_kwargs={'stage_name': 'Data Ingestion', 'pipeline_obj': DataIngestionTrainingPipeline, 'function_name': 'data_ingestion'},
    dag=dag,
)
 
# DAG for Data Preprocessing
data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing',
    python_callable=run_stage,
    op_kwargs={'stage_name': 'Data Preprocessing', 'pipeline_obj': DataPreprocessingTrainingPipeline, 'function_name': 'preprocessing_stage'},
    dag=dag,
)
 
# DAG for Data Modelling
data_modelling_task = PythonOperator(
    task_id='data_modelling',
    python_callable=run_stage,
    op_kwargs={'stage_name': 'Data Modelling', 'pipeline_obj': DataModellingPipeline, 'function_name': 'modelling_stage'},
    dag=dag,
)
 
# DAG for Model Evaluation
model_evaluation_task = PythonOperator(
    task_id='model_evaluation',
    python_callable=run_stage,
    op_kwargs={'stage_name': 'Model Evaluation', 'pipeline_obj': ModelEvaluatePipeline, 'function_name': 'data_evaluate'},
    dag=dag,
)
 
# DAG for User Prediction
user_prediction_task = PythonOperator(
    task_id='user_prediction',
    python_callable=run_stage,
    op_kwargs={'stage_name': 'User Prediction', 'pipeline_obj': UserPredictPipeline, 'function_name': 'user_predict'},
    dag=dag,
)
 
# Define the execution order of tasks
#data_ingestion_task >> data_preprocessing_task >> data_modelling_task >> model_evaluation_task >> user_prediction_task
user_prediction_task
 