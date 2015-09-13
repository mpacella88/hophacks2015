#simple scatter plot of addresses in tow data
import geopy
import numpy
import matplotlib.pyplot as plt
import csv
from geopy.geocoders import Nominatim

geolocator = Nominatim()

with open('/Users/mpacella/Downloads/DOT_Towing.csv') as f:
    reader = csv.reader(f)
    tow_list = list(reader)

#csv example
#import csv
#with open('/Users/mpacella/Downloads/DOT_Towing.csv') as f:
#    reader = csv.reader(f)
#    tow_list = list(reader)

longitude[]
latitude[]

for tow_data in tow_list:
    address = tow_data[10]
    location = geolocator.geocode(address)
    longitude.append(location.longitude)
    latitude.append(location.latitude)

plt.scatter(latitude,longitude)

plt.show()












