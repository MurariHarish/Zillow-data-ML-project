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
![Data Processing Pipeline Flowchart](Data_Pipeline_Flow.jpeg)
