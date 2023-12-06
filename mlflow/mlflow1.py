# import mlflow
from mlflow.models import infer_signature
from sklearn.metrics import roc_auc_score
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

search_space = {
    'max_depth' : scope.int(hp.quniform('max_depth', 4, 100, 1)),
    'learning_rate' : hp.loguniform('learning_rate', -3, 0),
    'reg_alpha' : hp.loguniform('reg_alpha', -5, -1),
    'reg_lambda' : hp.loguniform('reg_lambda', -6, -1),
    'min_child_length' : hp.loguniform('min_chilg_length', -1, 3),
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',
    'seed' : 123,
}

def model_training(params):
    mlflow.xgboost.autolog()
    # Load the diabetes dataset.
    # db = load_breast_cancer()
    # X_train, X_val, y_train, y_val = train_test_split(db.data, db.target)
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../dags/data/final.csv'))
    # Select relevant columns
    columns_to_use = ['indicator_id', 'region_id', 'year', 'month', 'CRAM', 'IRAM', 'LRAM', 'MRAM', 'NRAM', 'SRAM']

    # Define features and target variable
    X = df[columns_to_use]
    y = df['value']

    # Split the data into training and testing sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run(nested=True):
        train = xgb.DMatrix(data= X_train, label = y_train)
        validation = xgb.DMatrix(data = X_val, label = y_val)

        booster = xgb.train(params = params, dtrain = train, num_boost_round = 1000, \
                            evals = [(validation, 'validation')], early_stopping_rounds = 50)

        validation_predictions = booster.predict(validation)
        # auc_score = roc_auc_score(y_val, validation_predictions)
        # mlflow.log_metric('auc', auc_score)
        mse = mean_squared_error(y_val, validation_predictions)
        mlflow.log_metric('mse', mse)

        signature = infer_signature(X_train, booster.predict(train))
        mlflow.xgboost.log_model(booster, 'model', signature = signature)

        return {'status' : STATUS_OK, 'loss': mse, 'booster' : booster.attributes()}

def train_model(**kwargs):


    conf_spark = SparkConf().set("spark.driver.host", "127.0.0.1")
    sc = SparkContext(conf=conf_spark)

    spark_trails = SparkTrials(parallelism=6)

    with mlflow.start_run(run_name='xgboost_models'):
        best_parms = fmin(
            fn=model_training,
            space=search_space,
            algo=tpe.suggest,
            max_evals=2,
            trials=spark_trails,
        )


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


    # model_name = 'test_model'
    #
    # model_version = mlflow.register_model(f"runs:/{run_id}/random_forest_model", model_name)
    #
    # # Registering the model takes a few seconds, so add a small delay
    # time.sleep(15)

    # client.transition_model_version_stage(
    #     name=model_name,
    #     version=model_version.version,
    #     stage="Production",
    # )
    # print(mlflow.search_runs('attributes.status = ACTIVE').iloc[0])

    # for rm in client.search_registered_models(filter_string= "current_stage= Production"):
    #     print(dict(rm))

    # for rm in client.get_latest_versions('test_model',stages=['Production']):
    #     print(dict(rm))

# train_model()
# register_model()