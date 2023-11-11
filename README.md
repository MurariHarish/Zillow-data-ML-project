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
````commandline
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

Features comprise of 3 various sets of indicators.

- **10 ZHVI (Zillow House Value Index)** features

- **44 Inventory and sales** features

- **2 Rentals** features

## Data Pipeline:

- **Step-01: Extract the data**: Involves extracting the data in ZIP format from Nasdaq API with API key provided by the platform
- **Step-02: Load the data** :  Loading the extracted ZIP file to .csv format. Later read the .csv file into dataframe by chunks.
- **Step-03: Trim the data** : Cutting the data and considering only from year 2012, since computational power and storage for all 150M rows is very high.
- **Step-04: Changing date-time datatype** : Here we convert the date-time datatype to numeric to feed to the model
- **Step-05: Getting Interested Stats** : Out of all the Inventory and sales features, only few are relevant to most of the regions, so we consider those 6 features and pivot the table with region_id
- **Step-06: Merging the data with ZHVI features:** Now after we pivot we merge the ZHVI features to the pivoted stat features table from the above step. This step gives our final data that we use for our modelling purposes in future.

