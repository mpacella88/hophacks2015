#csv example
#import csv
#with open('/Users/mpacella/Downloads/DOT_Towing.csv') as f:
#    reader = csv.reader(f)
#    tow_list = list(reader)

#geopy example
#grab address and city fields from tow_list and pass to geolocator
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode(3957  BROOKLYN AVE BALTIMORE)
location.latitude
location.longitude




