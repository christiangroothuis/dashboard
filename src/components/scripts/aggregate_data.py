import pandas as pd
import os
from pathlib import Path

from map_categories import map_categories_dict

# Important directories
base_dir = os.path.join(Path(os.getcwd()).parent.parent.parent.parent)
data_directory = os.path.join(Path(os.getcwd()).parent.parent.parent.parent, 'data')

# Import data
df_pas_original = pd.read_csv(os.path.join(data_directory, 'pas_original.csv')).drop(columns='Unnamed: 0')
df_ss = pd.read_csv(os.path.join(data_directory, 'stop_search.csv')).drop(columns='Unnamed: 0')
df_street = pd.read_csv(os.path.join(data_directory, 'street.csv')).drop(columns='Unnamed: 0')
df_outcomes = pd.read_csv(os.path.join(data_directory, 'outcomes.csv')).drop(columns='Unnamed: 0')

# PAS DATA
trust_list = list()
confidence_list = list()

for i, attribute in map_categories_dict['PAS']['Trust']:
    trust_list.append(attribute)
for i, attribute in map_categories_dict['PAS']['Confidence']:
    confidence_list.append(attribute)
trust_confidence_list = trust_list + confidence_list
trust_confidence_list = list(dict.fromkeys(trust_confidence_list))

# df_trust = df_pas_original[['Borough', 'Year'] + trust_list]
df_pas_original['Trust'] = df_pas_original[trust_list].mean(axis=1)
df_pas_original['Confidence'] = df_pas_original[confidence_list].mean(axis=1)
df_pas_original['PAS'] = df_pas_original[trust_confidence_list].mean(axis=1)

# CRIME DATA
df_ss = df_ss.groupby(['Borough', 'Year'])['Type'].count().reset_index()
df_ss = df_ss.rename(columns={'Type': 'Stop&Search'})

df_street = df_street.groupby(['Borough', 'Year'])['Location'].count().reset_index()
df_street = df_street.rename(columns={'Location': 'StreetCrime'})

not_outcome_list = ['Unable to prosecute suspect',
            'Offender given absolute discharge',
            'Formal action is not in the public interest',
            'Defendant found not guilty',
            'Court case unable to proceed']
outcomes_relevant_columns = [col for col in df_outcomes.columns if col not in not_outcome_list]
outcomes_relevant_attributes = outcomes_relevant_columns.copy()
outcomes_relevant_attributes.remove('Borough')
outcomes_relevant_attributes.remove('Year')
df_outcomes['CrimeOutcomes'] = df_outcomes[outcomes_relevant_attributes].sum(axis=1)


# StopSearch, StreetCrime
def london_nan(dataframe):
    dataframe[dataframe['Borough'] == 'City of London'] = None
    return dataframe

df_ss = london_nan(df_ss)
df_street = london_nan(df_street)

# SAVE DATA
df_pas_original.to_csv(os.path.join(base_dir, 'data/pas_original_aggregated.csv'))
df_ss.to_csv(os.path.join(base_dir, 'data/stop_search_aggregated.csv'))
df_street.to_csv(os.path.join(base_dir, 'data/street_aggregated.csv'))
df_outcomes.to_csv(os.path.join(base_dir, 'data/outcomes_pivot.csv'))
