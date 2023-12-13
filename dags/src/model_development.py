# import mlflow
from mlflow.models import infer_signature

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes, load_breast_cancer
from hyperopt import fmin, tpe, hp, STATUS_OK
from hyperopt import SparkTrials
from hyperopt.pyll import scope
import mlflow.xgboost
import xgboost as xgb
from pyspark import SparkContext, SparkConf
from mlflow.tracking import MlflowClient
import time
from sklearn.metrics import mean_squared_error
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization,Dropout
from tensorflow.keras.optimizers import Adam
from kerastuner.tuners import RandomSearch
from tensorflow.keras.callbacks import TensorBoard
import datetime

def build_model(X_train, hp):
    model = Sequential()
    model.add(Dense(units=hp.Int('units_1', min_value=32, max_value=256, step=32),
                    activation='relu', input_shape=(X_train.shape[1],)))
    model.add(BatchNormalization())
    model.add(Dropout(hp.Float('dropout_1', min_value=0.2, max_value=0.5, step=0.1)))
    model.add(Dense(units=hp.Int('units_2', min_value=32, max_value=128, step=32),
                    activation='relu', kernel_regularizer='l2'))
    model.add(BatchNormalization())
    model.add(Dropout(hp.Float('dropout_2', min_value=0.2, max_value=0.5, step=0.1)))
    model.add(Dense(units=hp.Int('units_3', min_value=16, max_value=64, step=16),
                    activation='relu', kernel_regularizer='l2'))
    model.add(BatchNormalization())
    model.add(Dropout(hp.Float('dropout_3', min_value=0.2, max_value=0.5, step=0.1)))
    model.add(Dense(1, kernel_regularizer='l2'))

    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='log')),
        loss='mse')

    return model
def train_model(**kwargs):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/final.csv'))
    # Select relevant columns
    columns_to_use = ['indicator_id', 'region_id', 'year', 'month', 'CRAM', 'IRAM', 'LRAM', 'MRAM', 'NRAM', 'SRAM']

    # Define features and target variable
    X = df[columns_to_use]
    y = df['value']

    # Split the data into training and testing sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    log_dir = "../../tensorflow/logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch='5,10')

    with mlflow.start_run(run_name='NN_models'):
        tuner = RandomSearch(
                lambda hp: build_model(X_train, hp),
                objective='val_loss',
                max_trials=2,  # You can adjust the number of trials
                directory='tuner_logs',
                project_name='neural_network_tuning')
                # )

    tuner.search(X_train, y_train, epochs=5, validation_split=0.2,callbacks=[tensorboard_callback])

    # Get the best hyperparameters
    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

    # Build the model with the best hyperparameters
    best_model = tuner.hypermodel.build(best_hps)

    # Make predictions on the test set
    y_pred = best_model.predict(X_val)

    # Evaluate the model
    mse = mean_squared_error(y_val, y_pred)
    mlflow.log_metric('mse', mse)
    print(f'Mean Squared Error: {mse}')

    mlflow.tensorflow.log_model(best_model, 'model')

def register_model(**kwargs):

    model_name = 'test_model'
    #new run
    new_best_run = mlflow.search_runs(order_by=['metrics.mse DESC']).iloc[0]
    new_best_run_mse = new_best_run["metrics.mse"]
    new_best_run_id = new_best_run.run_id

    new_model_version = mlflow.register_model(f"runs:/{new_best_run_id}/model", model_name)
    time.sleep(15)

    print(f'MSE of Best Run: {new_best_run["metrics.mse"]}')
    print(new_best_run_id)

    # old run
    client = MlflowClient()
    try:

        old_run_id = client.get_latest_versions('test_model',stages=['Production'])[0].run_id
        old_run_version = client.get_latest_versions('test_model',stages=['Production'])[0].version
        # print(mlflow.search_runs(filter_string=f"attributes.run_id = '{old_run_id}'"))
        # if old_run_id is not None:
        if old_run_id == new_best_run_id:
            print("Old model is either better or equal")
            client.transition_model_version_stage(
                name=model_name,
                version=new_model_version.version,
                stage='Staging'
            )
        else:
            old_run = mlflow.search_runs(filter_string=f"attributes.run_id = '{old_run_id}'").iloc[0]

            client.transition_model_version_stage(
                name=model_name,
                version=old_run_version,
                stage='Archived'
            )

            client.transition_model_version_stage(
                name=model_name,
                version=new_model_version.version,
                stage='Production'
                )

    except:

        client.transition_model_version_stage(
            name=model_name,
            version=new_model_version.version,
            stage='Production'
        )

train_model()
register_model()