import os
from pathlib import Path
import numpy as np
from pyproj import Proj

# Internal imports
from .pas_data import import_clean_PAS_data, restructure_PAS_data
from .geo_borough import import_geo_borough_data, project_convert


# Variables
data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
inProj = Proj('epsg:27700')
outProj = Proj(proj='latlong', datum='WGS84')

# PAS import
df_data = import_clean_PAS_data(data_directory)
pas_categories = df_data['Measure'].unique()
pas_boroughs = df_data['Borough'].unique()
df_data, pas_boroughs = restructure_PAS_data(df_data, pas_categories, pas_boroughs)

# GEO data
if not os.path.isfile(os.path.join(data_directory, 'London_Boroughs_extracted.geojson')):
    geo_data, _ = import_geo_borough_data(data_directory, 'London_Boroughs.geojson')
    project_convert(geo_data, data_directory, source='epsg:27700', target='latlong', datum='WGS84')
geo_data, geo_boroughs = import_geo_borough_data(data_directory, 'London_Boroughs_extracted.geojson')

# Check if the borough names are identical at last
pas_boroughs.sort()
geo_boroughs.sort()
if np.array_equal(pas_boroughs, geo_boroughs):
    print("Identical Borough names!")
else:
    print("NOT identical Borough names!")
