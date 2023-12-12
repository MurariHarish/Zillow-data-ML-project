## Zillow Housing Data Analysis
### Overview

- The goal of the project is to create a machine learning model and a smooth CI / CD
pipeline for estimating house prices across diverse US areas. Given the underlying
monthly data frequency, this project uses the vast Zillow Real Estate Data, which is
updated weekly.
- Through this project, we can offer insightful information on the property market so
that both buyers and sellers may make wise choices. Accurate house price
forecasting is crucial for sellers, purchasers, and real estate investors. It can also
help financial organizations determine the worth of properties for mortgage purposes



### Getting Started:
These instructions will give you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on deploying the project on a live system.
### Prerequisites:

To build, test, and deploy this project, you will need:

- **Airflow** to schedule and run pipelines
- **Python** to code pipelines and data science
- **Docker** to package and containerize
- **DVC** to version data and ML models
- **Git/GitHub** for source code management

### Installing:
**1. Cloning the repository**
````command line
https://github.com/MurariHarish/Zillow-data-ML-project
````
**2. Create a conda environment after opening the repository**

```bash
conda create -n zillowvenv python=3.8 -y
```

```bash
conda activate zillowvenv
```

**3. Install the dependencies**
```bash
pip install -r requirements.txt
```
**4. Docker**
```commandline
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```
echo "AIRFLOW_HOME_DIR=$(pwd)" >> .env
```
 ```   
docker compose up airflow-init
```
```
docker compose up
```
## Data
The Zillow Real Estate Data (ZILLOW) is a
comprehensive dataset that provides real estate market indicators for 78,200+
regions across the United States. It includes 56 crucial metrics, such as market
indices, sales data, and inventories. This dataset is highly relevant for real estate
professionals, investors, and analysts to gain insights into the U.S. housing
market's dynamics.

The data is basically of 3 tables
Zillow_Data:

Features comprise 3 various sets of indicators.

- **10 ZHVI (Zillow House Value Index)** Features

- **44 Inventory and sales** Features

- **2 Rentals** Features

## Data Pipeline:

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

## User Installation

Welcome to the Zillow Data ML Project! Follow these instructions to get this project running on your local machine for development and testing. If you're planning on deploying this project in a live environment, refer to our deployment guidelines.

### Prerequisites

Before you begin, ensure you have the following tools installed and ready:

- **Airflow**: For scheduling and orchestrating the data pipelines.
- **Python**: For writing pipelines and data science scripts.
- **Docker**: Essential for packaging the project into containers, making it easy to deploy in AWS.
- **DVC**: Data Version Control, to manage and version the datasets and ML models.
- **Git/GitHub**: To clone the repository and manage the project's source code.

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
