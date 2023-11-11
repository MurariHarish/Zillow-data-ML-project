from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from ZillowHouseData.components.data_ingestion import DataIngestionTrainingPipeline
from ZillowHouseData.components.data_preprocessing import DataPreprocessingTrainingPipeline

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
    schedule_interval=timedelta(days=30),  # Set your desired schedule interval
)

def run_data_ingestion():
    obj = DataIngestionTrainingPipeline()
    obj.main()

data_ingestion_task = PythonOperator(
    task_id='data_ingestion_task',
    python_callable=run_data_ingestion,
    dag=dag,
)


data_ingestion_task >> data_preprocessing_task
