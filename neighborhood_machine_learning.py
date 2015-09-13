from sklearn.svm import SVR
import numpy as np
from sklearn import cross_validation
import scipy.stats as stat
import matplotlib.pyplot as plt
import itertools

#OK, we are going to enumerate all pairwise possible combinations and save a pretty correlation plot for each

#load dataset from pickle
geo_data = np.load("geo_machine_learning_data.npy")

#hard-code which columns are which features (UPDATE THIS ONCE HENRY IS FINISHED!!!!)
#order is rats,crime,speedcam,vaclots,liqlic,farm, houseperm
column_feature_mapping = {'liqLic':0 , 'vacLots':1, 'crime':2, 'housePerm':3, 'speedCam':4, 'farMarket':5, 'counts_minor':6, 'counts_HTC':7, 'counts_rat':8}

i=1
#iterate through all possible pairwise combinations of feature, one is the classifier, one is the target
for pair in itertools.combinations(column_feature_mapping.keys(),2):

    #create target (a 1D numpy array based on the attribute the user provides)
    #dimension should be n_bins
    target = geo_data[:,column_feature_mapping[pair[0]]]
    print target

    #create data (a 2D numpy array based on the classifiers the user provides)
    #dimensions should be n_bins x n_classifiers
    data = geo_data[:,[column_feature_mapping[pair[1]]]]
    print data


    clf = SVR()
    training_data, testing_data, training_target, testing_target = cross_validation.train_test_split(data, target, test_size = 0.4, random_state = 0)

    clf.fit(training_data, training_target)
    print clf.score(testing_data, testing_target)
    data = geo_data[:,column_feature_mapping[pair[1]]]
    if pair[1]=='farMarket':
        print 'farmarket data:'
        print data
    
    corr_coefficent = stat.pearsonr(data,target)
    print corr_coefficent[0]
    plt.figure(i)
    plt.scatter(data,target)
    plt.xlabel(pair[1])
    plt.ylabel(pair[0])
    plt.title("Pearson Correlation: "+str(corr_coefficent[0])+"  SVR Score: "+str(clf.score(testing_data, testing_target)))
    plt.savefig(pair[1]+"_"+pair[0]+".png")
    i+=1



#given a user-provided list of features this should read from the open baltiore
#database and count/average the feature for a particular geographic grid square over all
#data points

#given a user-provided grid square attribute this will create a target for
#SVR supervised learning

#the neighborhood features will then be used to train an SVM to predict some attribute
#about a neighborhood based on the desired features

#I think we may need to pass the hard-coded column value for a particular data table in order
#to get the counts for the feature

#may want a separate one-off script to create a table of counts for each feature in each grid square!!!
#assuming we have this for now







