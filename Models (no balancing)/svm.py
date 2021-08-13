#!/usr/bin/env python3

import os
import tarfile
import urllib
import pandas as pd
import sklearn
import numpy as np
import matplotlib.pyplot as plt

#loading in data
def load_labeled_data(csv_path):
    '''
        loads the labeled .csv dataset
        
        Args:
            csv_path (str): path to folder containing relevant datasets
        
        Returns:
             pd.DataFrame
    '''
    
    labeled_path = os.path.join(csv_path, "202113041556_labeledData.csv")
    return pd.read_csv(labeled_path)

ld = load_labeled_data(".")
ld_tr = ld.drop('Path', axis=1)

#loading in data
def load_features(csv_path):
    '''
        loads the features .csv dataset

        Args:
            csv_path (str): path to folder containing relevant datasets

        Returns:
            pd.DataFrame
    '''
    features_path = os.path.join(csv_path, "202113041556_all_features.csv")
    return pd.read_csv(features_path, low_memory=False, header=1)

fd = load_features(".")

from sklearn.metrics import confusion_matrix
import itertools

def draw_confusion_matrix(y, yhat, classes):
    '''
        Draws a confusion matrix for the given target and predictions
        Adapted from scikit-learn and discussion example.
    '''
    plt.cla()
    plt.clf()
    matrix = confusion_matrix(y, yhat)
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    num_classes = len(classes)
    plt.xticks(np.arange(num_classes), classes, rotation=90)
    plt.yticks(np.arange(num_classes), classes)
    
    fmt = 'd'
    thresh = matrix.max() / 2.
    for i, j in itertools.product(range(matrix.shape[0]), range(matrix.shape[1])):
        plt.text(j, i, format(matrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if matrix[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.show()

# split dataset for training and testing
from sklearn.model_selection import train_test_split
train, test, target, target_test = train_test_split(fd, ld_tr, test_size=0.2, random_state=0)

# SVM
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn import metrics

svc = make_pipeline(SVC(probability=True))
svc.fit(train, np.ravel(target))
svc_predicted = svc.predict(test)

print('Accuracy: ' + str(metrics.accuracy_score(target_test, svc_predicted)))
print('Precision: ' + str(metrics.precision_score(target_test, svc_predicted)))
print('Recall: ' + str(metrics.recall_score(target_test, svc_predicted)))
print('F1 Score: ' + str(metrics.f1_score(target_test, svc_predicted)))

print('Confusion Matrix:')
draw_confusion_matrix(target_test, svc_predicted, ["Not Obfuscated", "Obfuscated"])
