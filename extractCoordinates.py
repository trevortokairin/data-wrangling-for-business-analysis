import re
import pandas as pd


def extractCoordinates(dat):
    # verify that the two columns exist: 1) station 2) coordinates
    if 'station' not in dat.columns:
        return -1
    if 'coordinates' not in dat.columns:
        return -2

    # extract the latitude and longitude string values and convert to numeric values
    dat['lat'] = dat['coordinates'].apply(lambda x: float(re.findall(r'[-+]?\d*\.\d+|\d+', x)[0]))
    dat['lon'] = dat['coordinates'].apply(lambda x: float(re.findall(r'[-+]?\d*\.\d+|\d+', x)[1]))

    # returns our new data frame with new columns
    return dat[['station', 'lat', 'lon']]




