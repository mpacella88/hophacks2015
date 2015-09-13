from copy import copy
import os
import pandas as pd
import re

class DBDF(object):
    timePeriods = ['year', 'quarter', 'week', 'dayofyear']
    
    def __init__(self, csvPaths, dateCol='createdDate', descCol=u'codeDescription', latCol='latitude', longCol='longitude', neighborHoodCol='Neighborhood'):
        self.dateCol = dateCol
        self.descCol = descCol
        self.latCol = latCol
        self.longCol = longCol 
        self.neighborHoodCol = neighborHoodCol
        
        if isinstance(csvPaths, str):
            csvPaths = [csvPaths]
        self.csvPaths = []
        tmpDF = []
        for csvPath in csvPaths:
            self.csvPaths.append(os.path.realpath(csvPath))
            tmpDF.append(pd.read_csv(self.csvPaths[-1], quotechar='''"''', quoting=1, error_bad_lines=False))
            
        self.df = pd.concat(tmpDF, ignore_index=False)
        
    def select(self, text, invert=False, col=None):
        if col is None:
            col = self.descCol
        retVal = copy(self)
        if invert:
            selector = self.df[col].str.contains(text, flags=re.IGNORECASE)==0
        else:
            selector = self.df[col].str.contains(text, flags=re.IGNORECASE) > 0
        retVal.df = self.df[selector]
        return retVal
    
    def selectEq(self, cmpVal, col=None):
        if col is None:
            col = self.descCol
        retVal = copy(self)
        retVal.df = self.df.loc[self.df[col] == cmpVal]
        return retVal
    
    def sort(self, col=None):
        if col is None:
            col = self.dateCol
            
        self.df.sort(columns=col, inplace=True)
            
    def addTimeCols(self):
        self.df[self.dateCol] = pd.to_datetime(self.df[self.dateCol], infer_datetime_format=True)
        
        for timePeriod in self.timePeriods:
            self.df[timePeriod] = self.df[self.dateCol].map(lambda x: x.__getattribute__(timePeriod))
        
    def ratify(self):
        self = self.select('\Wrat\W')
        self = self.select('No Active Rodent', col='outcome', invert=True)
        self.sort()
        self.addTimeCols()
        return self
    
    def to_csv(self, outCsvPath, columns=None, sep=' '):
        if columns is None:
            self.df.to_csv(outCsvPath, sep=sep, header=False, index=False)
        else:
            self.df.to_csv(outCsvPath, columns=columns, sep=sep, header=False, index=False)
    
    def to_csv_ByTime(self, outCsvTmpl, timePeriod, sep=' '):
        for yr in [2014, 2015]:
            yrDF = self.selectEq(cmpVal=yr, col='year')
            for i,t in enumerate(yrDF.df[timePeriod].unique()):
                tDF = yrDF.selectEq(cmpVal=t, col=timePeriod)
                tDF.to_csv(outCsvTmpl % (timePeriod, i), columns=['latitude', 'longitude'])
    
if __name__=='__main__':
    dbDF = DBDF(['311_Customer_Service_Requests_with_lat_long_part_1.csv',
                 '311_Customer_Service_Requests_with_lat_long_part_2.csv',
                 '311_Customer_Service_Requests_with_lat_long_part_3.csv',
                 '311_Customer_Service_Requests_with_lat_long_part_4.csv'])
    dbDF = dbDF.ratify()
    dbDF.to_csv_ByTime('rats_%s_%d.csv', timePeriod='dayofyear')
    dbDF.to_csv('rats_all.csv', columns=['latitude', 'longitude'])
