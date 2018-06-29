#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 08:23:41 2018

@author: crazytrau
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
            if count[curLabel] < 10:
                count[curLabel]+=1
                if (numberItem > 0):
                    for tweetJson in data:
                        tweetJson = data[tweetJson]
                        dataset.append([trendingTopic[3], tweetJson['tweet'].replace("RT ","")])
    dataset = np.array(dataset)
    df = pd.DataFrame(data=dataset[0:,0:],    # values
                 columns=['Product', 'Consumer complaint narrative'])

    from io import StringIO
    col = ['Product', 'Consumer complaint narrative']
    df = df[col]
    df = df[pd.notnull(df['Consumer complaint narrative'])]
    df.columns = ['Product', 'Consumer_complaint_narrative']
    df['category_id'] = df['Product'].factorize()[0]
    category_id_df = df[['Product', 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['category_id', 'Product']].values)
    df.head()

    import matplotlib.pyplot as plt
#    fig = plt.figure(figsize=(8,6))
    print(df.groupby('Product').Consumer_complaint_narrative.count())
#    df.groupby('Product').Consumer_complaint_narrative.count().plot.bar(ylim=0)
#    plt.show()

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    features = tfidf.fit_transform(df.Consumer_complaint_narrative).toarray()
    labels = df.category_id
    features.shape
    
#    X=features
#    y=labels

    from sklearn.feature_selection import chi2
    import numpy as np
    N = 10
    for Product, category_id in sorted(category_to_id.items()):
      features_chi2 = chi2(features, labels == category_id)
      indices = np.argsort(features_chi2[0])
      feature_names = np.array(tfidf.get_feature_names())[indices]
      unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
      bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
      print("# '{}':".format(Product))
      print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
      print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.naive_bayes import MultinomialNB
    X_train, X_test, y_train, y_test = train_test_split(df['Consumer_complaint_narrative'], df['Product'], random_state = 0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)
    print('-------------',clf.predict(count_vect.transform(["That news today: world will destroyed"])))

    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import LinearSVC
    from sklearn.model_selection import cross_val_score
    models = [
        RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
        LinearSVC(),
        MultinomialNB(),
        LogisticRegression(random_state=0),
    ]
    CV = 5
    cv_df = pd.DataFrame(index=range(CV * len(models)))
    entries = []
    for model in models:
      model_name = model.__class__.__name__
      accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
      for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))
    cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
    import seaborn as sns
    sns.boxplot(x='model_name', y='accuracy', data=cv_df)
    sns.stripplot(x='model_name', y='accuracy', data=cv_df,
                  size=8, jitter=True, edgecolor="gray", linewidth=2)
    plt.show()

    print(cv_df.groupby('model_name').accuracy.mean())
