#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 08:23:41 2018

@author: crazytrau

guide https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
"""

# import library
import json
import csv
import numpy as np
import pandas as pd

def toLabel(label):
    if label =='ongoing-event':
        return 0
    elif label =='news':
        return 1
    elif label =='meme':
        return 2
    elif label =='commemorative':
        return 3

#main function
if __name__ == '__main__':
    # main variable
    dataset = []
    count = [0,0,0,0]
    #read every trending and export json file
    with open('../../data/TT-annotations.csv', newline='', encoding="utf8") as csvfile:
        trendingTopicArr = csv.reader(csvfile, delimiter=';')
        for trendingTopic in trendingTopicArr:
            path='../../../features/'+trendingTopic[0]+'.json'
            data = json.load(open(path))
            numberItem = len(data)
            curLabel = toLabel(trendingTopic[3])
            if count[curLabel] < 30:
                count[curLabel]+=1
                if (numberItem > 0):
                    for tweetJson in data:
                        tweetJson = data[tweetJson]
                        dataset.append([trendingTopic[3], tweetJson['tweet'].replace("RT ","")])
    dataset = np.array(dataset)
    df = pd.DataFrame(data=dataset[0:,0:],    # values
                 columns=['label', 'tweet'])

    from io import StringIO
    col = ['label', 'tweet']
    df = df[col]
    df = df[pd.notnull(df['tweet'])]
    df.columns = ['label', 'tweets']
    df['label_id'] = df['label'].factorize()[0]
    label_id_df = df[['label', 'label_id']].drop_duplicates().sort_values('label_id')
    label_to_id = dict(label_id_df.values)
    id_to_category = dict(label_id_df[['label_id', 'label']].values)
    df.head()

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8,6))
    print(df.groupby('label').tweets.count())
    df.groupby('label').tweets.count().plot.bar(ylim=0)
    plt.show()

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    features = tfidf.fit_transform(df.tweets).toarray()
    labels = df.label_id
    features.shape

    from sklearn.feature_selection import chi2
    import numpy as np
    N = 10
    for label, label_id in sorted(label_to_id.items()):
      features_chi2 = chi2(features, labels == label_id)
      indices = np.argsort(features_chi2[0])
      feature_names = np.array(tfidf.get_feature_names())[indices]
      unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
#      bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
      print("# '{}':".format(label))
      print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
#      print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.naive_bayes import MultinomialNB
    X_train, X_test, y_train, y_test = train_test_split(df['tweets'], df['label'], random_state = 0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#    clf = MultinomialNB().fit(X_train_tfidf, y_train)
#    print('-------------',clf.predict(count_vect.transform(["News to day: The world will destroy"])))

    from sklearn.svm import SVC
    classifier = SVC(kernel = 'linear', probability = True)
    classifier.fit(X_train_tfidf, y_train)
    import pickle
    with open('SVM_BagofWords.pkl', 'wb') as fout:
        pickle.dump(classifier, fout)

    # Predicting the Test set results
    X_test_counts = count_vect.transform(X_test)
    y_pred = classifier.predict(X_test_counts)
    #probality of sample
    class_probabilities = classifier.predict_proba(X_test_counts)
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
