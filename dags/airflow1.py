# # Import necessary libraries and modules
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# from src.data_pre_processing import download_data, load_data, data_preprocessing,get_year_month, get_stats, get_merge

# from airflow import configuration as conf

# # Enable pickle support for XCom, allowing data to be passed between tasks
# conf.set('core', 'enable_xcom_pickling', 'True')

# # Define default arguments for your DAG
# default_args = {
#     'owner': 'Dheeraj',
#     'start_date': datetime(2023, 11, 10),
#     'retries': 0, # Number of retries in case of task failure
#     'retry_delay': timedelta(minutes=5), # Delay before retries
# }

# # Create a DAG instance named 'your_python_dag' with the defined default arguments
# dag = DAG(
#     'your_python_dag',
#     default_args=default_args,
#     description='Your Python DAG Description',
#     schedule_interval=None,  # Set the schedule interval or use None for manual triggering
#     catchup=False,
# )

# # Define PythonOperators for each function

# # Task to load data, calls the 'load_data' Python function
# # download_data_task = PythonOperator(
# #     task_id='download_data_task',
# #     python_callable=download_data,
# #     dag=dag,
# # )
# # # Task to load data, calls the 'load_data' Python function
# # load_data_task = PythonOperator(
# #     task_id='load_data_task',
# #     python_callable=load_data,
# #     dag=dag,
# # )
# # Task to perform data preprocessing, depends on 'load_data_task'
# data_preprocessing_task = PythonOperator(
#     task_id='data_preprocessing_task',
#     python_callable=data_preprocessing,
#     dag=dag,
# )
# # Task to build and save a model, depends on 'data_preprocessing_task'
# get_year_month_task = PythonOperator(
#     task_id='get_year_month_task',
#     python_callable=get_year_month,
#     op_args=[data_preprocessing_task.output],
#     provide_context=True,
#     dag=dag,
# )
# # Task to load a model using the 'load_model_elbow' function, depends on 'build_save_model_task'
# get_stats_task = PythonOperator(
#     task_id='get_stats_task',
#     python_callable=get_stats,
#     op_args=[ get_year_month_task.output],
#     dag=dag,
# )

# # Task to load a model using the 'load_model_elbow' function, depends on 'build_save_model_task'
# get_merge_task = PythonOperator(
#     task_id='get_merge_task',
#     python_callable=get_merge,
#     op_args=[ get_stats_task.output],
#     dag=dag,
# )


# # Set task dependencies
# data_preprocessing_task >> get_year_month_task >> get_stats_task >> get_merge_task

# # If this script is run directly, allow command-line interaction with the DAG
# if __name__ == "__main__":
#     dag.cli()


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
    op_args=['src.data_pre_processing', 'download_data'],
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

# Set task dependencies
download_data_task >> load_data_task >> data_preprocessing_task >> get_year_month_task >> get_stats_task >> get_merge_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
