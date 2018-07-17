import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost", "htduongdl96", "motorola", "DBtweet")
# prepare a cursor object using cursor() method
cursor = db.cursor()
arrVectors = []

cursor.execute("select DEPTH_RETWEETS,RATIO_RETWEETS,HASHTAGS,\
        LENGTH, EXCLAMATIONS, QUESTIONS,LINKS  ,TOPICREPETITION  ,REPLIES   ,\
        SPREADVELOCITY   ,USER_DIVERSITY  ,RETWEETED_USER_DIVERSITY  ,HASHTAG_DIVERSITY ,\
        LANGUAGE_DIVERSITY  ,VOCABULARY_DIVERSITY  ,CLASS from TWEET_VECTOR_TRAIN")
row = cursor.fetchone()
while row is not None:
    # print(row)
    arrVectors.append(row)
    row = cursor.fetchone()
# print(arrVectors[0])

columns = [
                'depth_retweets',
                  'ratio_retweets',
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

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.DataFrame(arrVectors, columns=columns)
X = dataset.iloc[:,0:-1].values
y = dataset.iloc[:, 15].values
# print(X[1])
from sklearn.svm import SVC
import pickle
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
# classifier = SVC(kernel = 'linear', probability = True)
# classifier.fit(X, y)
# with open('model.pkl', 'wb') as fout:
#     pickle.dump(classifier, fout)

# load model from file:

with open('model.pkl', 'rb') as fin:
    classifier = pickle.load(fin)
    count = 0
    test = [9.02650e-02,9.02650e-02,2.46018e-01,7.77345e+01,2.35398e-01,1.16814e-01,5.31000e-03,
                                 9.27434e-01, 1.13274e-01, 1.47100e-03, 6.17858e+00, 5.71997e-01, 1.26287e+00,
                                 5.68029e-01, 5.17708e+01]
    # y_pred = classifier.predict([test])
    class_probabilities = classifier.predict_proba([test])
    print(class_probabilities.max(1)[0])



# filename = 'finalized_model.sav'
# joblib.dump(classifier, filename)
# print(X[0][0])
# print(y)
