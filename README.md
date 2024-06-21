# Polocal Dashboard
This repository contains the code of group 7 for the TU/e course JBG050 Data Challenge 2.


## Usage guide
> **Info:** Tested and supported Python version: 3.12

### Installation
To set up and run the project, follow the following steps:

1. Run `curl  "https://groothuis.cloud/s/qMyBcFctWtZk2GB/download" -o data.zip` to download the data necessary for running the dashboard
2. Use `unzip data.zip` to extract the downloaded data to the `data` folder
3. Clone this repository to your local machine.
4. `cd` into the project directory.
5. Create a virtual environment using `python -m venv venv` and activate it or use your preferred method.
6. Run `pip install -r requirements.txt` to install the required packages.
7. Run `cd src` to go to the `src` directory
8. Run `python app.py` to start running the dashboard


## Data
To reproduce the whole data preprocessing procedure, follow these steps:

### PAS granular data
1. Download the PAS granular data (shared by course coordinators), and place it in `data/pas_data_ward_level` subfolder.
2. Run src/data_preprocessing/pas_data_cleaning.py. The preprocessed PAS granular data will be saved in pas_proportions.csv in the `data` folder.

### PAS data
1. Download the PAS data from https://data.london.gov.uk/dataset/mopac-surveys (the file is called: PAS_T&Cdashboard_toQ3 23-24.xlsx). Place it in the `data` folder and convert it to pas_original_raw.csv.

### Ethnicity data
1. Download the data from https://data.london.gov.uk/dataset/ethnic-groups-borough.
2. Place it in the `data` folder.
3. Run src/data_preprocessing/ethnicity_data_cleaning.py. The preprocessed ethnicity data will be saved in ethnicity.csv in the `data` folder.

### Crime data
1. From https://data.police.uk/data/archive/ download "December 2017" and "December 2020". Unzip the folders into `data/original_crime_data`.
2. From https://data.police.uk/data/ download the data with the following specification: 
- Date range: January 2021 to December 2021
- Forces: Metropolitan Police Service
- Data sets: include crime data, include outcomes data, include stop and search data
Unzip the folder into `data/original_crime_data`.
3. Run src/data_preprocessing/crime_data_cleaning.py. The combined data will be saved in outcomes_combined.csv, ss_combined.csv, and street_combined.csv in the `data/crime_data` subfolder.
4. Download the data from https://data.london.gov.uk/dataset/london_boroughs in the gpkg format. Place it in the `data` folder.
5. Run src/data_preprocessing/crime_data_preprocessing.py. The combined data will be saved in outcomes.csv, s.csv, and street.csv in the `data` folder. Note: This will take a couple of hours.

### Economic data
1. Download the data from https://data.london.gov.uk/dataset/jobs-and-job-density-borough, https://data.london.gov.uk/dataset/average-income-tax-payers-borough, https://data.london.gov.uk/dataset/employment-industry-borough, https://data.london.gov.uk/dataset/employment-self-employed-full-time-and-part-time-and-gender-borough, https://data.london.gov.uk/dataset/economic-activity-gender, and https://data.london.gov.uk/dataset/economic-inactivity-gender. Place it in the `data/economic-data`.
2. Run ....... . The joined data will be saved in economic.csv in the `data` subfolder.

Once you have completed the above steps, do the final steps.
1. Run src/components/scripts/aggregate_data.py.
2. Run src/components/scripts/data_preprocessing.py.

Now you should have all the data needed to run the dashboard.
