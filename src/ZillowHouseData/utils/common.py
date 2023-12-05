import os, pickle, keras
import yaml
from src.ZillowHouseData.logger import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def load_keras_model(load_folder, file_name):
    try:
        # Create the full load path, including the "artifacts/" folder
        load_path = os.path.join("artifacts", load_folder, file_name)

        # Load the keras model file
        loaded_model = keras.models.load_model(load_path)

        return loaded_model

    except Exception as e:
        print(f"Error loading the model: {str(e)}")


def load_pickle_object(load_folder, file_name):
    try:
        # Create the full load path, including the "artifacts/" folder
        load_path = os.path.join("artifacts", load_folder, file_name)

        # Load the model from the pickle file
        with open(load_path, 'rb') as file:
            loaded_model = pickle.load(file)

        return loaded_model

    except Exception as e:
        print(f"Error loading the model: {str(e)}")

@ensure_annotations
def save_model_to_keras(keras_model, save_folder, file_name):
    try:
        # Create the full save path, including the "artifacts/" folder
        save_path = os.path.join("artifacts", save_folder, file_name)

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        keras_model.save(save_path)

        print(f"Model saved to {save_path}")
    except Exception as e:
        print(f"Error saving the model: {str(e)}")

@ensure_annotations       
def save_object_to_pickle(object_to_save, save_folder, file_name):
    try:
        # Create the full save path, including the "artifacts/" folder
        save_path = os.path.join("artifacts", save_folder, file_name)

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the trained model to a pickle file
        with open(save_path, 'wb') as file:
            pickle.dump(object_to_save, file)

        print(f"Model saved to {save_path}")
    except Exception as e:
        print(f"Error saving the model: {str(e)}")