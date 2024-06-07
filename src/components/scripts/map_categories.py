import pandas as pd
import os
from pathlib import Path

# data import
data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')

df_outcomes = pd.read_csv(os.path.join(data_directory, 'data_dc2/crime_data/outcomes_final.csv'))
df_ss = pd.read_csv(os.path.join(data_directory, 'data_dc2/crime_data/ss_final.csv'))
df_street = pd.read_csv(os.path.join(data_directory, 'data_dc2/crime_data/street_final.csv'))

# Get relevant attributes
outcome_types = df_outcomes['outcome_type'].unique()

ss_gender = ['Male:Female']
ss_age_range = df_ss['age_range'].unique()
ss_officer_def_ethnicity = df_ss['officer_def_ethinicty'].unique()
ss_legislation = df_ss['legislation'].unique()
ss_search_object = df_ss['search_object'].unique()
ss_outcome = df_ss['outcome'].unique()

street_crime_type = df_street['crime_type'].unique()
street_last_out_cat = df_street['last_out_cat'].unique()


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
        'PAS-Granular': [(str(111), 'Test1')],
        'Other': [('8', "Contact ward officer"),
                  ('9', "Trust MPS")],
    },
    'Economic':{
        'Demographic': [
            (str(112), 'Number of Individuals'),
        ],
        'Industry types': [
            (str(113), 'Manufacturing'),
            (str(114), 'Constructing'),
            (str(115), 'Hotels and Restaurants'),
            (str(116), 'Transport and Communication'),
            (str(117), 'Banking and Finance'),
            (str(118), 'Public Administration, Education and Health'),
            (str(119), 'Other Services'),
        ],
        'Employment': [
            (str(120), 'Job Density'),
            (str(121), 'Employed Ratio'),
            (str(122), 'Self-Employed Ratio'),
            (str(123), 'Full-Time Ratio'),
            (str(124), 'Part-Time Ratio'),
            (str(125), 'Active:Inactive'),
            (str(126), 'Active:Inactive Male'),
            (str(127), 'Active:Inactive Female'),
        ]
    },
    'Stop&Search': {
                'Male:Female': [(str(128), None)],
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
