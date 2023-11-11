from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from ZillowHouseData.components.data_ingestion import DataIngestion
from ZillowHouseData.components.data_preprocessing import DataPreprocessing
from ZillowHouseData.pipeline.stage_02_data_preprocessing import DataPreprocessingTrainingPipeline
from ZillowHouseData.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline

default_args = {
    'owner': 'MLflow_Keshav',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_data_pipeline',
    default_args=default_args,
    description='A simple Airflow DAG for data ingestion and preprocessing',
    schedule_interval=timedelta(days=2),  # Set your desired schedule interval
)

def run_data_ingestion():
    obj = DataIngestionTrainingPipeline()
    obj.data_ingestion()

def run_data_preprocessing():
    obj = DataPreprocessingTrainingPipeline()
    obj.main()

data_ingestion_task = PythonOperator(
    task_id='data_ingestion_task',
    python_callable=run_data_ingestion,
    dag=dag,
)

data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=run_data_preprocessing,
    dag=dag,
)

data_ingestion_task >> data_preprocessing_task