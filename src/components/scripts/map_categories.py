import pandas as pd
import os
from pathlib import Path

# data import
data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')

outcome_types = pd.read_csv(os.path.join(data_directory, 'outcomes_pivot.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns
ss_age_range = pd.read_csv(os.path.join(data_directory, 'age_range.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns
ss_officer_def_ethnicity = pd.read_csv(os.path.join(data_directory, 'officer_def_ethnicity.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns
ss_legislation = pd.read_csv(os.path.join(data_directory, 'legislation.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns
ss_search_object = pd.read_csv(os.path.join(data_directory, 'search_object.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns
ss_outcome = pd.read_csv(os.path.join(data_directory, 'ss_outcome.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns
street_crime_type = pd.read_csv(os.path.join(data_directory, 'crime_type.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns
street_last_out_cat = pd.read_csv(os.path.join(data_directory, 'ss_last_outcome.csv')).drop(columns=['Year', 'Borough', 'Unnamed: 0']).columns

df_outcomes = pd.read_csv(os.path.join(data_directory, 'outcomes_pivot.csv'))

pas_questions = ['SS Agree', 'SS Fair', 'Crime Victim', 'Officer Contact', 'Met Trust',
        'Police Accountable', 'Met Career', 'Gangs', 'Law Obligation', 'Area Living Time',
        'Crime Local Worry', 'Informed Local', 'Informed London', 'Asb Worry', 'Guns',
        'Knife Crime', 'People Trusted', 'People Courtesy', 'People Help', 'Call Suspicious',
        'Different Backgrounds', 'Good Job Local', 'Good Job London', 'Police Reliance',
        'Police Respect', 'Police Fair Treat', 'Community Matter', 'Local Concerns']

# Define list of tuples
def define_tuple_lists(offset, category):
    category_tuple_list = [(str(i + offset), name) for i, name in enumerate(category)]
    offset = int(category_tuple_list[-1][0]) + 1

    return category_tuple_list, offset


offset = 10

pas_questions_tuple_list, offset = define_tuple_lists(offset, pas_questions)
print(offset)

offset = 56

ss_age_range_tuple_list, offset = define_tuple_lists(offset, ss_age_range)
print(offset)

ss_officer_def_ethnicity_tuple_list, offset = define_tuple_lists(offset, ss_officer_def_ethnicity)
print(offset)

ss_legislation_tuple_list, offset = define_tuple_lists(offset, ss_legislation)
print(offset)

ss_search_object_tuple_list, offset = define_tuple_lists(offset, ss_search_object)
print(offset)

ss_outcome_tuple_list, offset = define_tuple_lists(offset, ss_outcome)
print(offset)

street_crime_type_tuple_list, offset = define_tuple_lists(offset, street_crime_type)
print(offset)

street_last_out_cat_type_tuple_list, offset = define_tuple_lists(offset, street_last_out_cat)
print(offset)

outcomes_tuple_list, offset = define_tuple_lists(offset, outcome_types)
print(offset)


# Dictionary
map_categories_dict = {
    'PAS': {
        'Confidence': [('0', '"Good Job" local'),
                       ('1', "Informed local"),
                       ('2', "Listen to concerns"),
                       ('3', "Relied on to be there"),
                       ('4', "Understand issues")],
        'Trust': [('5', "Listen to concerns"),
                  ('6', "Relied on to be there"),
                  ('7', "Treat everyone fairly")],
        'Other': [('8', "Contact ward officer"),
                  ('9', "Trust MPS")],
        'PAS-Granular': pas_questions_tuple_list,
    },
    'Economic':{
        'Demographic': [
            (str(38), 'White'),
            (str(39), 'Asian'),
            (str(40), 'Black'),
            (str(41), 'Mixed Other'),
            (str(42), 'Total'),
        ],
        'Industry types': [
            (str(43), 'Manufacturing (%)'),
            (str(44), 'Constructing (%)'),
            (str(45), 'Hotels and Restaurants (%)'),
            (str(46), 'Transport and Communication (%)'),
            (str(47), 'Banking and Finance (%)'),
            (str(48), 'Public Administration, Education and Health (%)'),
            (str(49), 'Other Services (%)'),
        ],
        'Employment': [
            (str(50), 'Job Density (%)'),
            (str(51), 'Employed (%)'),
            (str(52), 'Self-Employed (%)'),
            (str(53), 'Full-Time:Part-time'),
            (str(54), 'Active:Inactive Male'),
            (str(55), 'Active:Inactive Female'),
        ]
    },
    'Stop&Search': {
                'Age Range': ss_age_range_tuple_list,
                "Officer Defined Ethnicity": ss_officer_def_ethnicity_tuple_list,
                "Legislation": ss_legislation_tuple_list,
                'Search Object': ss_search_object_tuple_list,
                "Stop and Search Outcome": ss_outcome_tuple_list, },
    'StreetCrime': {
            'Crime Type Street': street_crime_type_tuple_list,
            'Last Outcome': street_last_out_cat_type_tuple_list,
        },
    'CrimeOutcomes': outcomes_tuple_list,
}
