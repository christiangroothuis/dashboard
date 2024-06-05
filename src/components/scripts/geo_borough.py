import os
import geojson
from pyproj import Proj, transform
import json


def import_geo_borough_data(data_directory, file):
    # Define the geodata
    with open(os.path.join(data_directory, file)) as f:
        geo_data = geojson.load(f)

    # Get borough names of the geodata
    borough_geo_data = list()
    for borough_data in geo_data['features']:
        borough_geo_data.append(borough_data['properties']['name'])
    return geo_data, borough_geo_data


def project_convert(geo_data, data_directory, source='epsg:27700', target='latlong', datum='WGS84'):
    """
    Takes a geojson dictionary and converts it from relative epsg locations to universal latlong.
    :param geo_data: geojson dictionary.
    :param data_directory: path to data directory.
    :param source: the location data format in geo_data.
    :param target: the location data format after transformation.
    :param datum: the relationship of a coordinate system to the body
    :return: nothing. Instead, writes data to a file.
    """
    inProj = Proj(source)
    outProj = Proj(proj=target, datum=datum)

    for i, borough in enumerate(geo_data['features']):
        print(i)
        for j, coordinate in enumerate(borough['geometry']['coordinates'][0]):
            x1, y1 = coordinate
            x2, y2 = transform(inProj, outProj, x1, y1)
            long_lat = [x2, y2]
            borough['geometry']['coordinates'][0][j] = long_lat

    # Write the modified GeoJSON object to a file (optional)
    with open(os.path.join(data_directory, 'London_Boroughs_extracted.geojson'), 'w') as outfile:
        json.dump(geo_data, outfile)