__author__ = 'Henry'

import pandas as pd
import os
import requests
import numpy as np

def data_assemble():
    #data_311 = get_data("https://data.baltimorecity.gov/resource/9agw-sxsr.csv")           # Works !! Can get GPS Data !!
    #employee_data_14 = get_data("https://data.baltimorecity.gov/resource/2j28-xzd7.csv")   # Works
    crime_data = get_data("https://data.baltimorecity.gov/resource/3i3v-ibrt.csv")         # Works
    #parking_citation = get_data("https://data.baltimorecity.gov/resource/n4ma-fj3m.csv")   # Works !! Can get GPS Data !!
    #property_taxes = get_data("https://data.baltimorecity.gov/resource/27w9-urtv.csv")     # Works !! Can get GPS Data !!
    #vacant_building = get_data("https://data.baltimorecity.gov/resource/qqcv-ihn5.csv")    # Works
    #liquor_license = get_data("https://data.baltimorecity.gov/resource/xv8d-bwgi.csv")     # Works

    # This part I will write out csv files in to be loaded as a function of time
    coor = extract_long_lat1(crime_data)
    date = list(crime_data['ArrestDate'])
    write_time_data(date,coor)

    #test_dat0 = extract_long_lat2(liquor_license)
    #test_dat = extract_long_lat1(vacant_building)
    #test_dat2 = extract_long_lat1(crime_data)
    #counts_liquor = bin_balt(-76.681240,39.373947,-0.147814,0.10631,10,10,test_dat0)
    #counts_vacant = bin_balt(-76.681240,39.373947,-0.147814,0.10631,10,10,test_dat)
    #counts_crime = bin_balt(-76.681240,39.373947,-0.147814,0.10631,10,10,test_dat2)
    #test = np.hstack((counts_liquor.reshape((100,1)),counts_vacant.reshape((100,1)),counts_crime.reshape((100,1))))
    #print
    #print test
    print
    np.save("geo_machine_learning_data",test)
    return

def write_time_data(date,coor):
    for x in range(0,len(coor)):
        if int(date[x][3:5]) == 5:
            outfile = open('crime7.csv','a')
            outfile.write("%f %f\n"%(coor[x][0],coor[x][1]))
        elif int(date[x][3:5]) == 4:
            outfile = open('crime6.csv','a')
            outfile.write("%f %f\n"%(coor[x][0],coor[x][1]))
        elif int(date[x][3:5]) == 3:
            outfile = open('crime5.csv','a')
            outfile.write("%f %f\n"%(coor[x][0],coor[x][1]))
        elif int(date[x][3:5]) == 2:
            outfile = open('crime4.csv','a')
            outfile.write("%f %f\n"%(coor[x][0],coor[x][1]))
        elif int(date[x][3:5]) == 1:
            outfile = open('crime3.csv','a')
            outfile.write("%f %f\n"%(coor[x][0],coor[x][1]))
        elif int(date[x][3:5]) == 31:
            outfile = open('crime2.csv','a')
            outfile.write("%f %f\n"%(coor[x][0],coor[x][1]))
        elif int(date[x][3:5]) == 30:
            outfile = open('crime1.csv','a')
            outfile.write("%f %f\n"%(coor[x][0],coor[x][1]))

# This is a function that extracts long and lat for
#   vacant_building and crime_data
def extract_long_lat1(data_set):
    test_dat = []
    for x in data_set['Location 1']:
        if len(str(x)) > 10:
            test_dat.append([ float(y.strip()) for y in x[1:-1].split(',') ])
    return test_dat

# This function extract GPS data from the liquor license data set
def extract_long_lat2(data_set):
    test_dat = []
    for x in data_set['Location 1']:
        if len(str(x)) > 5:
            holder = x.split('\n')[-1].strip() #note this line may need to be changed going between windows/mac
            test_dat.append([ float(y.strip()) for y in holder[1:-1].split(',') ])
    return test_dat

def get_data(info_url):
    r = requests.get(info_url,verify=False)
    temp = open("temp.csv",'w')
    temp.write(r.text)
    raw_data = pd.read_csv('temp.csv')
    temp.close()
    os.remove('temp.csv')
    return raw_data

# Starting Point for lat and long
#   39.373947, -76.681240
# Minimum y and x
#   39.267637, -76.533426
# ylen = 0.10631
# xlen = -0.147814

# This is a function that will define the area which we can bin
#   the data by longitude and latitude. It will return a
#   numpy matrix of counts
def bin_balt(xstart,ystart,xlen,ylen,xbin,ybin,coordinates):
    deltax = xlen/float(xbin)
    deltay = ylen/float(ybin)
    counts = np.zeros((xbin,ybin))
    for pairs in coordinates:
        n = 1
        nx = 0
        ny = 0
        while ystart > pairs[0] and n <= ybin:
            #print (ystart-(n*deltay))
            if (ystart-(n*deltay)) > pairs[0]:
                nx = n-1
            n += 1
        n = 1
        while xstart < pairs[1] and n <= xbin:
            #print (xstart - (n*deltax))
            if (xstart - (n*deltax)) < pairs[1]:
                ny = n-1
            n += 1
        counts[nx][ny] += 1
    return counts

data_assemble()