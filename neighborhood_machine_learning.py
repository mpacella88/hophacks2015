from sklearn.svm import SVR
import numpy as np
from sklearn import cross_validation

import argparse

#argument parsing
'''parser = argparse.ArgumentParser(description='grabbing user-provided list of classifiers and single attribute for prediction')
parser.add_argument('--feature_to_predict', help='provide the feature to predict')
parser.add_argument('--features_to_train_against', help='provide the features for training ')
parser.add_argument('--path_to_pickled_dataset', help='provide the path to the pickled dataset')
args = parser.parse_args()'''

#load dataset from pickle
geo_data = np.load("geo_machine_learning_data.npy")

#create target (a 1D numpy array based on the attribute the user provides)
#dimension should be n_bins
target = geo_data[:,0]


#create data (a 2D numpy array based on the classifiers the user provides)
#dimensions should be n_bins x n_classifiers
data = geo_data[:,1:3]


clf = SVR()
training_data, testing_data, training_target, testing_target = cross_validation.train_test_split(data, target, test_size = 0.4, random_state = 0)

clf.fit(training_data, training_target)
print clf.score(testing_data, testing_target)



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







