#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:46:50 2018

@author: crazytrau
"""
# import library
import json
import csv
from generateFeature import generateFeature

#main function
if __name__ == '__main__':
    # main variable
    trendingTopicArr=[]

    data = json.load(open('output.json'))
    arrVectors = []

    toCur = False

    #read every trending and export json file
    with open('../../data/TT-annotations.csv', newline='', encoding="utf8") as csvfile:
        trendingTopicArr = csv.reader(csvfile, delimiter=';')
        for trendingTopic in trendingTopicArr:
            path='../../../features/'+trendingTopic[0]+'.json'
            temp = generateFeature(trendingTopic[2], path, trendingTopic[3])
#            print(trendingTopic[3])
            if temp != None: arrVectors.append(temp)
            
    columns = [   'ratio_retweets',
                  'hashtags',
                  'length',
                  'exclamations',
                  'questions',
                  'links',
                  'topicRepetition',
                  'replies',
                  'spreadVelocity',
                  'user_diversity',
                  'retweeted_user_diversity',
                  'hashtag_diversity',
                  'language_diversity',
                  'vocabulary_diversity',
                  'class']
            
# Support Vector Machine (SVM)

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.DataFrame(arrVectors, columns=columns)
X = dataset.iloc[:,0:-1].values
y = dataset.iloc[:, 14].values

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
models = [
#    RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
    LinearSVC(),
    MultinomialNB(),
    LogisticRegression(random_state=0),
    SGDClassifier(loss="hinge", penalty="l2"),
#    MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1),
    KNeighborsClassifier(3),
    SVC(kernel="linear"),
    SVC(gamma=2, C=1),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()
]
CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
  model_name = model.__class__.__name__
  accuracies = cross_val_score(model, X, y, scoring='accuracy', cv=CV)
  for fold_idx, accuracy in enumerate(accuracies):
    entries.append((model_name, fold_idx, accuracy))
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
import seaborn as sns
sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df,
              size=3, jitter=True, edgecolor="gray", linewidth=1)
plt.xticks(rotation=90)
plt.show()

print(cv_df.groupby('model_name').accuracy.mean())

classifier = GaussianProcessClassifier(1.0 * RBF(1.0))

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', probability = True)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
#probality of sample
class_probabilities = classifier.predict_proba(X_test)
#array of percent, real label, pred label
temp = np.stack((class_probabilities.max(1), y_test, y_pred), axis=-1)

abc = np.asarray(list(filter(lambda sample: sample[0]>0.8, temp)))
abc = np.sort(abc, axis=0)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix,cohen_kappa_score
#cm = confusion_matrix(y_test, y_pred, labels=[0,1])
#cohen_kappa_score(y_test, y_pred, labels=[0,1])
cm = confusion_matrix(y_test, y_pred)
print(cohen_kappa_score(y_test, y_pred))

a=0
for i in range(0,len(y_pred)):
    if y_pred[i] == y_test[i]:
        a=a+1
print (a/len(y_pred))

## Visualising the Training set results
#from matplotlib.colors import ListedColormap
#X_set, y_set = X_train, y_train
#X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
#                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
#plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
#             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
#plt.xlim(X1.min(), X1.max())
#plt.ylim(X2.min(), X2.max())
#for i, j in enumerate(np.unique(y_set)):
#    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
#                c = ListedColormap(('red', 'green'))(i), label = j)
#plt.title('SVM (Training set)')
#plt.xlabel('Age')
#plt.ylabel('Estimated Salary')
#plt.legend()
#plt.show()
#
## Visualising the Test set results
#from matplotlib.colors import ListedColormap
#X_set, y_set = X_test, y_test
#X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
#                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
#plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
#             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
#plt.xlim(X1.min(), X1.max())
#plt.ylim(X2.min(), X2.max())
#for i, j in enumerate(np.unique(y_set)):
#    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
#                c = ListedColormap(('red', 'green'))(i), label = j)
#plt.title('SVM (Test set)')
#plt.xlabel('Age')
#plt.ylabel('Estimated Salary')
#plt.legend()
#plt.show()















