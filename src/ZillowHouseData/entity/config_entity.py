from dataclasses import dataclass
from pathlib import Path
from typing import List
from datetime import date

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    source_URL : str
    local_data_file : Path
    unzip_dir : Path

@dataclass(frozen=True)
class DataPreprocessingConfig:
    file_name: str
    start_date: str
    interested_columns: List[str]
    interested_indicators_stats: List[str]
    interested_indicators_zhvi: List[str]
    stats_path: Path
    final_csv_path: Path

@dataclass(frozen=True)
# class ModelTrainingConfig:
    # learning_rate: float
    # epochs: int
    # batch_size: int
    # validation_split: float
    # verbose: int
    # final_csv_path: Path

class ModelTrainingConfig:
    max_depth: int
    learning_rate: float
    reg_alpha: float
    reg_lambda: int
    min_child_weight: int
    objective: str
    eval_metric: str
    n_estimators: int
    random_state: int
    final_csv_path: Path

@dataclass(frozen=True)
class UserPredictConfig:
    user_input_reqs: List[str]
