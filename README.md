# CS5530
# Name: Aslonjon Nosirov
# Assignment 1


## Data

The raw data represent information from 10 female participants, including their height (inches), weight (pounds), age (years), grip strength (kilograms), and a qualitative frailty indicator, Y and N.

*   Source: Manually provided table in the problem description.
*   Location:** `data_raw/raw_data.csv`

## Workflow Stages

### 1. Ingest

*   The raw data, as provided in the problem description's table, will be saved into `data_raw/raw_data.csv`.
*   This CSV file will then be read into a pandas DataFrame within the `data_processing.py` script.

### 2. Process

The `data_processing.py` script will perform the following transformations:

#### a. Unit Standardization
*   `Height_m`: Calculated as `Height_in * 0.0254`
*   `Weight_kg`: Calculated as `Weight_lb * 0.45359237`

#### b. Feature Engineering
*   `BMI`: Calculated as `Weight_kg / (Height_m ** 2)` and rounded to 2 decimals.
*   `AgeGroup`: Categorical variable derived from `Age_yr`, with categories: "<30", "30-45", "46-60", ">60".

#### c. Categorical → Numeric Encoding
*   `Frailty_binary`: Binary encoding of `Frailty` (Y→1, N→0), stored as `int8`.
*   One-hot encoding of `AgeGroup` into new columns: `AgeGroup_<30`, `AgeGroup_30-45`, `AgeGroup_46-60`, `AgeGroup_>60`.

The processed data will be saved to `data_processed/processed_data.csv`.

### 3. Analyze

The `analysis.py` script will perform the following:

#### a. EDA & Reporting
*   Compute summary statistics (mean, median, standard deviation) for all numeric columns.
*   Save the summary table to `reports/findings.md`.

#### b. Quantify Relation of Strength & Frailty
*   Compute the correlation between `Grip_kg` and `Frailty_binary`.
*   Report this correlation in `reports/findings.md`.

 
## Reports

The `reports/findings.md` file will contain the summary statistics and the correlation analysis results.

## Application

Python 3.12.3
VS Code (Version:1.104.2)
OS Windows 11
