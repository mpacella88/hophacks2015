from inspect import isclass
from itertools import cycle
import geopy
import numpy as np
import os
import pandas as pd
from time import sleep

from geopy.geocoders import ArcGIS
from geopy.geocoders import Bing
from geopy.geocoders import OpenMapQuest
# from geopy.geocoders import GoogleV3
# from geopy.geocoders import Nominatim
_geocoderTypes = [Geocoder for Geocoder in vars().values() if isclass(Geocoder) and issubclass(Geocoder, geopy.geocoders.base.Geocoder)]

class GeoCodr(object):
    def __init__(self,
                 csvPath,
                 bing_api_key,#='Asd8oy3X0l2q3ZR8sNV-yivQBBik-MP_m7UhQHjICIZipiQmeq6EAQOz2l4GJh2K', 
#                 google_api_key='AIzaSyCYsHk9XQpmo1qcSgiqZaVrvzDjhGDInMQ',
                 timeout=5,
                 workUnitNum=None):
        self.csvInPath = os.path.realpath(csvPath)
        self.csvOutPath = ''.join(os.path.realpath(csvPath).split('.')[:-1]) + '_with_lat_long.csv'
        
        self.bing_api_key = bing_api_key
#         self.google_api_key =google_api_key
        self.timeout = timeout
        
        self.read_csv()
        self.initGeocoderCycle()
        
        self.workUnitNum = int(workUnitNum)
        if self.workUnitNum is not None:
            self.chunkLen = len(self.df)/4
            wuSlice = slice(self.workUnitNum*self.chunkLen, (self.workUnitNum+1)*self.chunkLen)
            self.df = self.df[wuSlice]
        
        self.inStartRow = self.csvResume()
        self.flushRows = 50
    
    def csvResume(self):
        if os.path.isfile(self.csvOutPath):
            with open(self.csvOutPath) as tmpOut:
                tmpOut.seek(-(2**15), 2)
                for line in tmpOut:
                    pass
                last = line
            lastTokens = last.split(',')
            print int(lastTokens[0])
            return int(lastTokens[0])
        else:
            return self.df.index[0]
          
    def read_csv(self):
        self.df = pd.read_csv(self.csvInPath)
        
        self.df['codedAddress'] = ''
        self.df['latitude'] = 0.0
        self.df['longitude'] = 0.0
    
    def to_csv(self, sep=',', startRow=None, endRow=None):
        dfSlice = slice(startRow, endRow)
        if not os.path.isfile(self.csvOutPath):
            self.df[dfSlice].to_csv(self.csvOutPath, mode='a', index=False, sep=sep)
        elif len(self.df[dfSlice].columns) != len(pd.read_csv(self.csvOutPath, nrows=1, sep=sep).columns):
            raise Exception("Columns do not match!! Dataframe has " + str(len(self.df[dfSlice].columns)) + " columns. CSV file has " + str(len(pd.read_csv(self.csvOutPath, nrows=1, sep=sep).columns)) + " columns.")
        elif not (self.df[dfSlice].columns == pd.read_csv(self.csvOutPath, nrows=1, sep=sep).columns).all():
            raise Exception("Columns and column order of dataframe and csv file do not match!!")
        else:
            self.df[dfSlice].to_csv(self.csvOutPath, mode='a', index=False, sep=sep, header=False)
    
    def initGeocoderCycle(self):
        self.geocoders = []
        for Geocoder in _geocoderTypes:
            kwargs = {'timeout':self.timeout}
            if 'Bing' in Geocoder.__name__:
                kwargs['api_key'] = self.bing_api_key
            elif 'Google' in Geocoder.__name__:
                kwargs['api_key'] = self.google_api_key
            self.geocoders.append(Geocoder(**kwargs))
        self.geocoderCycle = cycle(self.geocoders)
        
    def geocode(self, colName='address'):
        i = self.inStartRow
        running = True
        for geocoder in self.geocoderCycle:
            if running==False:
                break
            print 'switching Geocoder to %s' % geocoder.__class__.__name__
            while True:
                if i>self.df.index[-1]:
                    running = False
                    break
                elif i%self.flushRows==0 and i!=0:
                    print 'processing row %d' % i
                    self.to_csv(startRow=i-self.flushRows, endRow=i)
                try:
                    if 'Bing' in geocoder.__class__.__name__:
                        query = {'addressLine':self.df[colName][i], 'locality':'Baltimore', 'state':'Maryland'}
                    elif 'Google' in geocoder.__class__.__name__ or 'Nominatim' in geocoder.__class__.__name__:# or 'OpenMapQuest' in geocoder.__class__.__name__:
                        query = {'street':self.df[colName][i], 'city':'Baltimore', 'state':'Maryland'}
                    else:
                        query = self.df[colName][i] + 'Baltimore, Maryland'
#                     print query
                    location = geocoder.geocode(query)
                    self.df['codedAddress'][i] = location.address, 
                    self.df['latitude'][i] = float(location.latitude)
                    self.df['longitude'][i] = float(location.longitude)
                    i+=1
                except (AttributeError, TypeError) as e:
                    i+=1
                except geopy.exc.GeopyError:
                    switchSleep = 2
                    print 'Switching geocoder in %d seconds' % switchSleep
                    sleep(switchSleep)
                    i+=1
                    break
                    
if __name__=='__main__':
    import sys
    try:
        csvPath = sys.argv[1]
        bing_api_key = sys.argv[2]
        workUnitNum = sys.argv[3]
    except:
        print 'Usage: geoCodr csvPath bing_api_key workUnitNum'
        sys.exit()
    geoCodr = GeoCodr(csvPath, bing_api_key=bing_api_key, workUnitNum=workUnitNum)
    geoCodr.geocode(colName='address')
