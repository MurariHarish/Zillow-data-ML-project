# Zillow Real Estate Data (ZILLOW)

## Overview

The Zillow Real Estate Data (ZILLOW) data feed provides comprehensive real estate market indicators such as market indices, rental rates, sales figures, and inventory levels for thousands of geographical areas across the United States.

### Publisher

Zillow, a leader in real estate and rental marketplaces, is dedicated to empowering consumers with data, inspiration, and knowledge about their living spaces, and connecting them with top local professionals for assistance.

## Coverage & Data Organization

### Coverage

This data feed includes 10 indicators across 3 categories:
- Home Values
- Rentals
- Sales and Inventories

The covers over 700 regions in the U.S.

### Data Organization

The Project focussess on following Categories
- **Metro Area & USA**

## Access

This product is accessible via the Nasdaq Data Link's Tables API.

- **Web Access:** [Zillow Data on Nasdaq Data Link](https://data.nasdaq.com/databases/ZILLOW)

- **API Access:**
  ```plaintext
  https://data.nasdaq.com/api/v3/datatables/ZILLOW/DATA?qopts.export=true&api_key={API_KEY}
  ```
  Replace `{API_KEY}` with your actual API key.

### Python Access:

To access this data using Python, you can use the Quandl library. First, install the library using pip if you haven't already:

```bash
pip install quandl
```

Then, you can use the following script to access the data:

```python
import quandl
quandl.ApiConfig.api_key = '{API_KEY}'  # Replace with your actual API key
data = quandl.get_table('ZILLOW/DATA')
print(data)
```

Note: Ensure you replace `{API_KEY}` with your actual Quandl API key.


## Tables and Columns

### Tables

1. **Zillow Data (ZILLOW/DATA):** Values for all indicators.
2. **Zillow Indicators (ZILLOW/INDICATORS):** Names and IDs of all indicators.
3. **Zillow Regions (ZILLOW/REGIONS):** Names and IDs of all regions.

### Column Definitions

#### ZILLOW DATA (ZILLOW/DATA)
- `indicator_id` (String): Unique indicator identifier (Primary Key, Filterable)
- `region_id` (String): Unique region identifier (Primary Key, Filterable)
- `date` (Date): Date of data point
- `value` (Double): Value of data point

#### ZILLOW INDICATORS (ZILLOW/INDICATORS)
- `indicator_id` (String): Unique indicator identifier (Primary Key, Filterable)
- `indicator` (String): Name of indicator
- `category` (String): Category of indicator

#### ZILLOW REGIONS (ZILLOW/REGIONS)
- `region_id` (String): Unique region identifier (Primary Key, Filterable)
- `region_type` (String): Region type (Filterable)
- `region` (String): Region description (Filterable)

## User Installation Guide

Welcome to the Zillow Data ML Project! Follow these instructions to get this project running on your local machine for development and testing. If you're planning on deploying this project in a live environment, refer to our deployment guidelines.

### Prerequisites

Before you begin, ensure you have the following tools installed and ready:

- **Airflow**: For scheduling and orchestrating the data pipelines.
- **Python**: For writing pipelines and data science scripts.
- **Docker**: Essential for packaging the project into containers, making it easy to deploy in AWS.
- **DVC**: Data Version Control, to manage and version the datasets and ML models.
- **Git/GitHub**: To clone the repository and manage the project's source code.

# MLOps Tools Overview

In our project, we employ a suite of advanced tools to streamline our machine learning operations (MLOps). Each tool plays a critical role in the development, deployment, and maintenance of our machine learning models.

The tools used in our project include:

- GitHub Actions
- Docker
- Apache Airflow
- DVC (Data Version Control)
- Amazon Web Services (AWS)
- MLflow
- Flask

### Installation Steps

#### 1. Cloning the Repository

Start by cloning the repository to your local machine:

```command line
git clone https://github.com/MurariHarish/Zillow-data-ML-project
```

Navigate into the project directory:

```bash
cd Zillow-data-ML-project
```

#### 2. Setting Up the Environment

Create a new Conda environment specifically for this project:

```bash
conda create -n zillowvenv python=3.10 -y
```

Activate the newly created environment:

```bash
conda activate zillowvenv
```

#### 3. Installing Dependencies

Install all the required Python packages:

```bash
pip install -r requirements.txt
```

#### 4. Docker Configuration

Set up Docker environment variables:

```commandline
echo -e "AIRFLOW_UID=$(id -u)" > .env
echo "AIRFLOW_HOME_DIR=$(pwd)" >> .env
```

Initialize and start Airflow services using Docker Compose:

```commandline
docker compose up airflow-init
docker compose up
```

## Project Pipeline Structure

Here's an overview of the folder structure for the project:

```plaintext
Zillow-data-ML-project/
├── artifacts/
│   ├── models/
│   │   └── [model files]
├── dags/
│   ├── airflow_main.py
├── config/
│   └── config.yaml
├── .github/
│   └── workflows/
│       └── [workflow files]
├── templates/
│   └── index.html
├── notebook/
│   └── [jupyter notebooks]
├── src/
│   └── ZillowHouseData/
│       ├── pipeline/
│       ├── config/
│       ├── entity/
│       ├── constants/
│       ├── utils/
│       └── components/
├── main.py
├── app.py
├── setup.py
├── params.yaml
├── requirements.txt

```
## Data Processing Pipeline Flowchart
![Data Processing Pipeline Flowchart](templates/workflow.jpeg)

## Overview

# Data Ingestion Pipeline
The `DataIngestionPipeline` script orchestrates the data ingestion process for a machine learning project. This stage is crucial for acquiring the dataset before training the model. The script is structured as follows:

Data Ingestion Pipeline Overview
The data ingestion pipeline involves two main components:
stage_01_data_ingestion_pipeline.py
data_ingestion.py

Steps:
- Data Ingestion Pipeline Execution (stage_01_data_ingestion.py):
    Configuration Initialization: The script initializes the configuration manager and retrieves the data ingestion configuration.
    Data Ingestion Execution: The script then creates an instance of the DataIngestion class and triggers the download and extraction processes.

- Data Ingestion Configuration (data_ingestion.py):
  Download File: Fetches the data from the specified URL using the gdown library. The downloaded file is saved to the local filesystem.
  Extract Zip File: Unzip the downloaded file into the designated extraction directory. If the zip file contains nested zip files, they are also extracted. After extraction, the original zip files are deleted, leaving only the extracted data files.

# Data Preprocessing Pipeline
The `DataPreprocessingTrainingPipeline` script orchestrates the data preprocessing phase, ensuring the dataset is refined and structured for subsequent model training.

Data Preprocessing Pipeline Overview
The data ingestion pipeline involves two main components:
stage_02_data_preprocessing_pipeline.py
data_preprocessing.py

Steps:
- Read and Filter Data: The script reads the CSV file in chunks, filters rows based on the specified start date, and concatenates the filtered chunks into a single DataFrame.
- Extract Year and Month: A new DataFrame column for the year and month is created from the existing 'date' column.
- Get Statistics: Statistical indicators specified in the configuration are extracted, and a pivot table is created based on region, year, and month. The resulting DataFrame is saved to a CSV file.
- Merge DataFrames: DataFrames containing statistical indicators and monthly/yearly data are merged, creating a comprehensive dataset. The merged DataFrame is saved to a **final** CSV file.
- Extract Unique Regions: A dictionary mapping region IDs to region names is created and saved using pickling.

# Model Training Pipeline
The `DataModellingPipeline` script serves as the entry point for the model training pipeline. Its primary responsibilities include data preparation, model building, and training. The README provides insights into each stage of the pipeline.

Data Model Training Pipeline Overview
The data ingestion pipeline involves two main components:
stage_02_model_training_pipeline.py
model_training.py

Steps:
- Data Preparation: Read and preprocess the final dataset, preparing features (X), target (y), and label mapping.
- Train-Test Split and Pickling: Split the dataset into training and testing sets with scaled features. Pickle split data and the feature scaler.
- Model Training: construct a neural network model and train the model using the training dataset, logging training details. Save the trained model and essential parameters for evaluation.
- Perform hyperparameter tuning using the Keras Tuner library and Log the best hyperparameters for reference.

# Model Evaluation Pipeline
The `ModelEvaluatePipeline` class orchestrates the evaluation of the trained machine learning model. It achieves this by executing a series of steps:

- **Model Loading**: Retrieves the saved Keras model from the filesystem.
- **Data Preparation**: Loads the scaled test dataset (`X_test_scaled`) and the true labels (`y_test`).
- **Model Evaluation**: Utilizes the loaded model to predict the test data and computes performance metrics such as Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared (R2).

### Evaluation Metrics

The performance of the model is quantified using the following metrics:

- **Step-01: Extract the data**: Involves extracting the data in ZIP format from Nasdaq API with API key provided by the platform
- **Step-02: Load the data** :  Loading the extracted ZIP file to .csv format. Later read the .csv file into the dataframe in chunks.
- **Step-03: Trim the data** : Cutting the data and considering only from the year 2012, since computational power and storage for all 150M rows is very high.
- **Step-04: Changing date-time datatype** : Here we convert the date-time datatype to numeric to feed to the model
- **Step-05: Getting Interested Stats** : Out of all the Inventory and sales features, only a few are relevant to most of the regions, so we consider those 6 features and pivot the table with region_id
- **Step-06: Merging the data with ZHVI features:** Now after we pivot we merge the ZHVI features to the pivoted stat features table from the above step. This step gives the final data that we use for our modeling purposes in the future.

## Data Modelling

- **Step-01: Read the stored DataFrame from artifacts and prepare the data
- **Step-02: perform test-train split and scale the DataFrame to return the X_train, X_test, y_train, y_test and scaler files and save them as pickle files.
- **Step-03: build model using x_train_scaled.shape[1] as input to build the model.
- **Step-04: train the model by passing the X_train and y_train as arguments with learning rates and epochs passed from the ModelTrainingConfig class from the file configentity.
- **Step-05: Save the models directory as model.keras
- 
