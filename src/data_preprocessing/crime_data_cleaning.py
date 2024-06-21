import os
import numpy as np
import pandas as pd
from typing import Tuple


def combine_csv() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Combine multiple csv files of a known type for the Metropolitan Police Service.
    :returns: three dataframes with outcomes, stop-and-search, and street data, respectively.
    """

    known_types = ['outcomes', 'search', 'street']
    root_dir = '../data/original_crime_data'
    dfs = {}
    
    # Iterate over subfolders in the data folder
    for subfolder in os.listdir(root_dir):
        subfolder_path = os.path.join(root_dir, subfolder)
        
        # Check if the item in the data folder is a directory
        if os.path.isdir(subfolder_path):
            # Iterate over CSV files in the subfolder
            for csv_file in os.listdir(subfolder_path):
                if csv_file.endswith(".csv"):
                    csv_file_path = os.path.join(subfolder_path, csv_file)
                    
                    parts = csv_file[:-4].split('-')

                    type_ = next((part for part in parts if (part in known_types) and (parts[2] == 'metropolitan')), None)

                    if (parts[-1] == type_) and (parts[2] == 'metropolitan'):
                        df = pd.read_csv(csv_file_path)

                        if type_ not in dfs:
                            dfs[type_] = []

                        dfs[type_].append(df)
    
    # combine data by type
    for type_, dataframes in dfs.items():
        print(type_)

        if type_ == known_types[0]:
            outcomes_df = pd.concat(dataframes, ignore_index=True)
            print(outcomes_df.shape)
        elif type_ == known_types[1]:
            ss_df = pd.concat(dataframes, ignore_index=True)
            print(ss_df.shape)
        elif type_ == known_types[2]:
            street_df = pd.concat(dataframes, ignore_index=True)
            print(street_df.shape)

    return outcomes_df, ss_df, street_df

def clean_outcomes(outcomes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean outcomes data.
    :param outcomes_df: dataframe with outcomes
    :returns: dataframe with cleaned data.
    """
    # spilt date into month and year, add quarter
    outcomes_df['month'] = pd.to_datetime(outcomes_df['Month'])   
    outcomes_df['year'] = outcomes_df['month'].dt.year
    outcomes_df['month'] = outcomes_df['month'].dt.month
    outcomes_df['quarter'] = outcomes_df['month'].apply(lambda x: np.ceil(x/3))
    outcomes_df = outcomes_df.astype({'quarter': int}).copy()

    # remove irrelevant columns
    outcome_df = outcomes_df.drop(['Month', 'Reported by', 'Falls within'], axis=1)

    # remove duplicates
    no_duplicates = outcome_df.drop_duplicates(ignore_index=True)

    # check number of missing values per column
    for col in no_duplicates.columns:
        missing_values = no_duplicates[col].isna()
        print(f'Number of missing values in {col}: {missing_values.sum()}')

    # remove entries without location details
    nans_removed = no_duplicates.dropna(subset=['Longitude', 'Latitude'])
    
    # rename columns
    final_outcomes = nans_removed.rename(columns={'Crime ID': 'crime_id', 'Longitude': 'longitude', 'Latitude': 'latitude', 'Location': 'location', 'LSOA code': 'lsoa_code',
       'LSOA name': 'lsoa_name', 'Outcome type': 'outcome_type', 'month': 'month', 'year': 'year', 'quarter': 'quarter'})
    
    return final_outcomes

def clean_ss(ss_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean stop-and-search data.
    :param ss_df: dataframe with stop-and-search
    :returns: dataframe with cleaned data.
    """
    # spilt date into day, month, year and timestamp, add quarter
    ss_df['Date'] = pd.to_datetime(ss_df['Date'], format='ISO8601')
    ss_df['year'] = ss_df['Date'].dt.year
    ss_df['month'] = ss_df['Date'].dt.month
    ss_df['day'] = ss_df['Date'].dt.day
    ss_df['timestamp'] = ss_df['Date'].dt.timetz
    ss_df['quarter'] = ss_df['month'].apply(lambda x: np.ceil(x/3))

    # remove irrelevant columns
    relevant_col_df = ss_df.drop(['Date', 'Part of a policing operation', 'Policing operation', 'Outcome linked to object of search', 'Removal of more than just outer clothing'], axis=1)

    # remove duplicates
    no_duplicates_ss = relevant_col_df.drop_duplicates(ignore_index=True)

    # check number of missing values per column
    for col in no_duplicates_ss.columns:
        missing_values = no_duplicates_ss[col].isna()
        print(f'Number of missing values in {col}: {missing_values.sum()}')

    # remove entries without location details
    nans_removed = no_duplicates_ss.dropna(subset=['Longitude', 'Latitude'])

    # rename columns
    final_ss = nans_removed.rename(columns={'Type': 'type', 'Latitude': 'latitude', 'Longitude': 'longitude',
       'Gender': 'gender', 'Age range': 'age_range', 'Self-defined ethnicity': 'self_def_ethnicity',
       'Officer-defined ethnicity': 'officer_def_ethinicty', 'Legislation': 'legislation', 'Object of search': 'search_object',
       'Outcome': 'outcome', 'year': 'year', 'month': 'month', 'day': 'day', 'timestamp': 'timestamp'})
    
    return final_ss

def clean_street(street_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean street data.
    :param street_df: dataframe with street
    :returns: dataframe with cleaned data.
    """
    # spilt date into month and year, add quarter
    street_df['month'] = pd.to_datetime(street_df['Month'])   
    street_df['year'] = street_df['month'].dt.year
    street_df['month'] = street_df['month'].dt.month
    street_df['quarter'] = street_df['month'].apply(lambda x: np.ceil(x/3))
    street_df = street_df.astype({'quarter': int}).copy()

    # remove irrelevant columns
    street_df = street_df.drop(['Month', 'Reported by', 'Falls within', 'Context'], axis=1).copy()

    # remove duplicates
    no_duplicates = street_df.drop_duplicates(ignore_index=True)

    # check number of missing values per column
    for col in no_duplicates.columns:
        missing_values = no_duplicates[col].isna()
        print(f'Number of missing values in {col}: {missing_values.sum()}')

    # remove entries without location details
    nans_removed = no_duplicates.dropna(subset=['Longitude', 'Latitude'])
    
    # rename columns
    final_street = nans_removed.rename(columns={'Crime ID': 'crime_id', 'Longitude': 'longitude', 'Latitude': 'latitude', 'Location': 'location', 'LSOA code': 'lsoa_code',
       'LSOA name': 'lsoa_name', 'Crime type': 'crime_type', 'Last outcome category': 'last_out_cat', 'month': 'month', 'year': 'year', 'quarter': 'quarter'})
    
    return final_street

def save_df_to_csv(df: pd.DataFrame, type: str) -> None:
    """
    Save dataframe to csv in data/crime_data.
    :param df: dataframe to be saved
    :param type: type of the data to be saved, e.g. outcomes, stop-and-search, street
    """
    # path to the data folder
    data_folder = "../data/crime_data"

    # check if the directory exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print('The new directory is created!')

    # save dataframe
    df.to_csv(f'{data_folder}/{type}_combined.csv', index=False)
    print(f"CSV {type} saved.")

# load the data
outcomes_df, ss_df, street_df = combine_csv()

# clean the data
clean_outcomes_df = clean_outcomes(outcomes_df)
clean_ss_df = clean_ss(ss_df)
clean_street_df = clean_street(street_df)

print(f'Outcomes data: {clean_outcomes_df.shape}')
print(f'Stop and search data: {clean_ss_df.shape}')
print(f'Street data: {clean_street_df.shape}')

# save the data to csv
save_df_to_csv(clean_outcomes_df, 'outcomes')
save_df_to_csv(clean_ss_df, 'ss')
save_df_to_csv(clean_street_df, 'street')
