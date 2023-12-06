# Import necessary libraries and modules
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importing only at the top level can lead to slow DAG parsing, hence import inside functions

# Define default arguments for your DAG
default_args = {
    'owner': 'Dheeraj',
    'start_date': datetime(2023, 11, 10),
    'retries': 1,  # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=1),  # Delay before retries
}

# Create a DAG instance named 'your_python_dag' with the defined default arguments
dag = DAG(
    'your_python_dag',
    default_args=default_args,
    description='Your Python DAG Description',
    schedule_interval=None,  # Set the schedule interval or use None for manual triggering
    catchup=False,
)

# Define a function to import and call your module functions
def call_function(module_name, function_name, *args, **kwargs):
    import importlib
    module = importlib.import_module(module_name)
    func = getattr(module, function_name)
    return func(*args, **kwargs)

# Define PythonOperators for each function

# Task to perform data preprocessing

download_data_task= PythonOperator(
    task_id='download_data_task',
    python_callable=call_function,
    op_args=['src.data_ingestion', 'download_data'],
    dag=dag,
)

# Task to build and save a model, depends on 'data_preprocessing_task'
load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=call_function,
    op_args=['src.data_pre_processing', 'load_data'],
    provide_context=True,
    dag=dag,
)

data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=call_function,
    op_args=['src.data_pre_processing', 'data_preprocessing'],
    dag=dag,
)

# Task to build and save a model, depends on 'data_preprocessing_task'
get_year_month_task = PythonOperator(
    task_id='get_year_month_task',
    python_callable=call_function,
    op_args=['src.data_pre_processing', 'get_year_month'],
    provide_context=True,
    dag=dag,
)

# Task to load a model using the 'get_stats' function, depends on 'get_year_month_task'
get_stats_task = PythonOperator(
    task_id='get_stats_task',
    python_callable=call_function,
    op_args=['src.data_pre_processing', 'get_stats'],
    dag=dag,
)

# Task to perform the 'get_merge' function, depends on 'get_stats_task'
get_merge_task = PythonOperator(
    task_id='get_merge_task',
    python_callable=call_function,
    op_args=['src.data_pre_processing', 'get_merge'],
    dag=dag,
)

# Task to perform the 'get_merge' function, depends on 'get_merge_task'
get_data_to_model_task = PythonOperator(
    task_id='get_data_to_model_task ',
    python_callable=call_function,
    op_args=['src.data_pre_processing', 'get_data_to_model'],
    dag=dag,
)

# Task to perform the 'train_model_task' function, depends on 'get_data_to_model_task'
train_model_task = PythonOperator(
    task_id='train_model_task',
    python_callable=call_function,
    op_args=['src.model_development', 'train_model'],
    dag=dag,
)

# Task to perform the 'register_model_task' function, depends on 'train_model_task'
register_model_task = PythonOperator(
    task_id='register_model_task',
    python_callable=call_function,
    op_args=['src.model_development', 'register_model'],
    dag=dag,
)

# Set task dependencies
# download_data_task >> load_data_task >> data_preprocessing_task >> get_year_month_task >> get_stats_task >> get_merge_task >> train_model_task >> register_model_task
train_model_task >> register_model_task
# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
