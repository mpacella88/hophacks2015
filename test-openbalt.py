__author__ = 'Henry'

import pandas as pd
import os
import requests

def data_assemble():
    data_311 = get_data("https://data.baltimorecity.gov/resource/9agw-sxsr.csv")
    employee_data_14 = get_data("https://data.baltimorecity.gov/resource/2j28-xzd7.csv")
    crime_data = get_data("https://data.baltimorecity.gov/resource/3i3v-ibrt.csv")
    parking_citation = get_data("https://data.baltimorecity.gov/resource/n4ma-fj3m.csv")
    property_taxes = get_data("https://data.baltimorecity.gov/resource/27w9-urtv.csv")
    vacant_building = get_data("https://data.baltimorecity.gov/resource/qqcv-ihn5.csv")
    return

def get_data(info_url):
    r = requests.get(info_url,verify=False)
    temp = open("temp.csv",'w')
    temp.write(r.text)
    raw_data = pd.read_csv('temp.csv')
    temp.close()
    os.remove('temp.csv')
    return raw_data

data_assemble()