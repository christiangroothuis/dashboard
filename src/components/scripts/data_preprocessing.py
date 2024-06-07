import os
from pathlib import Path
import numpy as np
import pandas as pd

# Internal imports
from pandas import DataFrame

from pas_data import import_clean_PAS_data, restructure_PAS_data
from geo_borough import import_geo_borough_data, project_convert

# Variables
data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')

# ==================
# PAS data
# ==================
df_pas_original = import_clean_PAS_data(data_directory)  # All data check
pas_categories = df_pas_original['Measure'].unique()
pas_boroughs = df_pas_original['Borough'].unique()

# ==================
# Geo data
# ==================
# GEO data
if not os.path.isfile(os.path.join(data_directory, 'geojson/London_Boroughs_extracted.geojson')):
    geo_data, _ = import_geo_borough_data(data_directory, 'geojson/London_Boroughs.geojson')
    project_convert(geo_data, data_directory, source='epsg:27700', target='latlong', datum='WGS84')
geo_data, geo_boroughs = import_geo_borough_data(data_directory, 'geojson/London_Boroughs_extracted.geojson')

df_pas_original, pas_boroughs = restructure_PAS_data(df_pas_original, pas_categories, geo_boroughs)


# Check if the borough names are identical at last
pas_boroughs.sort()
geo_boroughs.sort()
if np.array_equal(pas_boroughs, geo_boroughs):
    print("Identical Borough names!")
else:
    print("NOT identical Borough names!")


# ==================
# Other imports
# ==================
def load_data(path) -> pd.DataFrame:
    """
    Load pas data with count for different answers per question, borough, and year.
    :returns: dataframe loaded from a csv file.
    """
    df = pd.read_csv(path)

    return df


def transform_string(dataframe):
    for column in dataframe.columns:
        replaced_string = column.replace("_", " ")
        capitalized_string = replaced_string.title()
        dataframe.rename(columns={column: capitalized_string}, inplace=True)

    try:
        dataframe.rename(columns={'Borough Name': 'Borough'}, inplace=True)
    except:
        dataframe.rename(columns={'Area': 'Borough'}, inplace=True)

    return dataframe


# Import and transform
df_pas_granular = transform_string(load_data(os.path.join(data_directory, 'pas_data/pas_granular.csv')))
df_outcomes = transform_string(load_data(os.path.join(data_directory, 'crime_data/outcomes.csv')))
df_stop_search = transform_string(load_data(os.path.join(data_directory, 'crime_data/stop_search.csv')))
df_street = transform_string(load_data(os.path.join(data_directory, 'crime_data/street.csv')))
df_economic_raw = load_data(os.path.join(data_directory, 'economic_data/joined-economic.csv'))
df_ethnicity = transform_string(pd.read_csv(os.path.join(data_directory, 'ethnicity_data/ethnicity.csv'), delimiter=';'))

df_economic_raw.replace('!', np.nan, inplace=True)

all_numeric = list(df_economic_raw.columns).copy()
all_numeric.remove('Area')
df_economic_num = df_economic_raw[all_numeric].apply(pd.to_numeric, errors='coerce')
df_economic_num['Borough'] = df_economic_raw['Area']

# Extract relevant columns from economic data, and change column names
extracted_index = ['Borough', 'Year']
extracted_columns_econ_percentage = ['manufacturing', 'construction', 'distribution_hotels_and_restaurants',
                                     'transport_and_communications', 'banking_finance_and_insurance',
                                     'public_admin_education_and_health_confidence', 'other_services_confidence',
                                     'job_density', 'total_employed', 'total_self_employed']
extracted_columns_econ_aggregated = ['Full-Time:Part-time', 'Active:Inactive Male', 'Active:Inactive Female']
extracted_columns_econ_num = ['Year'] + extracted_columns_econ_percentage + extracted_columns_econ_aggregated
extracted_columns_econ = extracted_index + extracted_columns_econ_percentage + extracted_columns_econ_aggregated

for column in extracted_columns_econ_percentage:
    if not np.issubdtype(df_economic_num[column].dtype, np.number):
        print(column, df_economic_num[column].dtype)
    df_economic_num[column] = df_economic_num[column] / df_economic_num['number_of_individuals']


df_economic_num['Full-Time:Part-time'] = df_economic_num['total_full_time'] / df_economic_num['total_part_time']
df_economic_num['Active:Inactive Male'] = df_economic_num['economically_active_male'] / df_economic_num[
    'Economically Inactive_male']
df_economic_num['Active:Inactive Female'] = df_economic_num['economically_active_female'] / \
                                            df_economic_num['Economically Inactive_female']

renamed_columns_econ = ['Borough', 'Year', 'Manufacturing (%)', 'Constructing (%)', 'Hotels and Restaurants (%)',
                        'Transport and Communication (%)', 'Banking and Finance (%)',
                        'Public Administration, Education and Health (%)', 'Other Services (%)',
                        'Job Density (%)', 'Employed (%)', 'Self-Employed (%)', 'Full-Time:Part-time',
                        'Active:Inactive Male', 'Active:Inactive Female']


column_mapping = {tup[0]: tup[1] for tup in zip(extracted_columns_econ, renamed_columns_econ)}

df_economic = df_economic_num[extracted_columns_econ]
df_economic.rename(columns=column_mapping, inplace=True)


# Include City of London everywhere, set all values to Nan

# Convert 'Date' column to datetime format
df_pas_original['Date'] = pd.to_datetime(df_pas_original['Date']).dt.year.astype(int)
df_pas_original.rename(columns={'Date': 'Year'}, inplace=True)

all_dfs = [df_pas_granular, df_outcomes, df_stop_search, df_street, df_economic, df_ethnicity]


all_dfc_w_London_city = []
for df in all_dfs:

    years = df['Year'].unique()
    # data_to_append = []

    for year in years:
        row_data = {'Year': year, 'Borough': 'City of London'}
        for column in df.columns:
            if column not in ['Year', 'Borough']:
                row_data[column] = float('nan')  # Set all other values to NaN
        # data_to_append.append(row_data)
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True, axis=0)
    all_dfc_w_London_city.append(df)


# Check if the borough names are identical at last
pas_boroughs = sorted(df_pas_original['Borough'].unique())
pas_granular_boroughs = sorted(all_dfc_w_London_city[0]['Borough'].unique())
outcomes_boroughs = sorted(all_dfc_w_London_city[1]['Borough'].unique())
ss_boroughs = sorted(all_dfc_w_London_city[2]['Borough'].unique())
street_boroughs = sorted(all_dfc_w_London_city[3]['Borough'].unique())
economic_boroughs = sorted(all_dfc_w_London_city[4]['Borough'].unique())
ethnicity_boroughs = sorted(all_dfc_w_London_city[5]['Borough'].unique())
all_boroughs = [geo_boroughs, pas_boroughs, pas_granular_boroughs, outcomes_boroughs, ss_boroughs, street_boroughs, economic_boroughs,
                ethnicity_boroughs]

for i, borough1 in enumerate(all_boroughs):
    for j, borough2 in enumerate(all_boroughs):

        if np.array_equal(borough1, borough2):
            pass
        else:
            print("NOT identical Borough names!")
            print(i, len(borough1), j, len(borough2))


# Fill all City of london to Nan in df_pas_original:
mask = df_pas_original['Borough'] == 'City of London'
columns_to_keep = ['Year', 'Borough']
df_pas_original.loc[mask, df_pas_original.columns.difference(columns_to_keep)] = np.nan

# Dataframes for export
geo_data = geo_data.copy()
df_pas_original = df_pas_original.copy()
df_pas_granular = all_dfc_w_London_city[0]
df_outcomes = all_dfc_w_London_city[1]
df_stop_search = all_dfc_w_London_city[2]
df_street = all_dfc_w_London_city[3]
df_economic = all_dfc_w_London_city[4]
df_ethnicity = all_dfc_w_London_city[5]


df_pas_original.to_csv(os.path.join(data_directory, 'data_processed/pas_original.csv'))
df_pas_granular.to_csv(os.path.join(data_directory, 'data_processed/pas_granular.csv'))

df_outcomes.to_csv(os.path.join(data_directory, 'data_processed/outcomes.csv'))
df_stop_search.to_csv(os.path.join(data_directory, 'data_processed/stop_search.csv'))
df_street.to_csv(os.path.join(data_directory, 'data_processed/street.csv'))

df_economic.to_csv(os.path.join(data_directory, 'data_processed/economic.csv'))
df_ethnicity.to_csv(os.path.join(data_directory, 'data_processed/ethnicity.csv'))
