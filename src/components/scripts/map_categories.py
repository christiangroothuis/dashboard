import pandas as pd
import os
from pathlib import Path

# data import
data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')

df_outcomes = pd.read_csv(os.path.join(data_directory, 'outcomes.csv'))
df_ss = pd.read_csv(os.path.join(data_directory, 'stop_search.csv'))
df_street = pd.read_csv(os.path.join(data_directory, 'street.csv'))

# Get relevant attributes
outcome_types = df_outcomes['Outcome Type'].unique()

# ss_gender = ['Male:Female']
ss_age_range = df_ss['Age Range'].unique()
ss_officer_def_ethnicity = df_ss['Officer Def Ethinicty'].unique()
ss_legislation = df_ss['Legislation'].unique()
ss_search_object = df_ss['Search Object'].unique()
ss_outcome = df_ss['Outcome'].unique()

street_crime_type = df_street['Crime Type'].unique()
street_last_out_cat = df_street['Last Out Cat'].unique()


# Define list of tuples
def define_tuple_lists(offset, category):
    category_tuple_list = [(str(i + offset), name) for i, name in enumerate(category)]
    offset = int(category_tuple_list[-1][0]) + 1

    return category_tuple_list, offset


offset = 10
outcomes_tuple_list, offset = define_tuple_lists(offset, outcome_types)

ss_age_range_tuple_list, offset = define_tuple_lists(offset, ss_age_range)
ss_officer_def_ethnicity_tuple_list, offset = define_tuple_lists(offset, ss_officer_def_ethnicity)
ss_legislation_tuple_list, offset = define_tuple_lists(offset, ss_legislation)
ss_search_object_tuple_list, offset = define_tuple_lists(offset, ss_search_object)
ss_outcome_tuple_list, offset = define_tuple_lists(offset, ss_outcome)

street_crime_type_tuple_list, offset = define_tuple_lists(offset, street_crime_type)
street_last_out_cat_type_tuple_list, offset = define_tuple_lists(offset, street_last_out_cat)

print(street_last_out_cat_type_tuple_list[-1])


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
        'PAS-Granular': [(str(114), 'Test1')],
        'Other': [('8', "Contact ward officer"),
                  ('9', "Trust MPS")],
    },
    'Economic':{
        'Demographic': [
            (str(115), 'White'),
            (str(116), 'Asian'),
            (str(117), 'Black'),
            (str(118), 'Mixed Other'),
            (str(119), 'Total'),
        ],
        'Industry types': [
            (str(120), 'Manufacturing (%)'),
            (str(121), 'Constructing (%)'),
            (str(122), 'Hotels and Restaurants (%)'),
            (str(123), 'Transport and Communication (%)'),
            (str(124), 'Banking and Finance (%)'),
            (str(125), 'Public Administration, Education and Health (%)'),
            (str(126), 'Other Services (%)'),
        ],
        'Employment': [
            (str(127), 'Job Density (%)'),
            (str(128), 'Employed (%)'),
            (str(129), 'Self-Employed (%)'),
            (str(130), 'Full-Time:Part-time'),
            (str(131), 'Active:Inactive Male'),
            (str(132), 'Active:Inactive Female'),
        ]
    },
    'Stop&Search': {
                # 'Male:Female': [(str(140), None)],
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
