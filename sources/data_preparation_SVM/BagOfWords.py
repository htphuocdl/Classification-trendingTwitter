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
    count =0
    #read every trending and export json file
    with open('../../data/TT-annotations.csv', newline='', encoding="utf8") as csvfile:
        trendingTopicArr = csv.reader(csvfile, delimiter=';')
        for trendingTopic in trendingTopicArr:
            path='../../../features/'+trendingTopic[0]+'.json'
            data = json.load(open(path))
            numberItem = len(data)
            print (numberItem)
            if (numberItem > 0):
                for tweetJson in data:
                    tweetJson = data[tweetJson]
                    dataset.append([trendingTopic[3], tweetJson['tweet']])
                    print (trendingTopic[3], tweetJson['tweet'])
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
    fig = plt.figure(figsize=(8,6))
    df.groupby('Product').Consumer_complaint_narrative.count().plot.bar(ylim=0)
    plt.show()

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    features = tfidf.fit_transform(df.Consumer_complaint_narrative).toarray()
    labels = df.category_id
    features.shape

    from sklearn.feature_selection import chi2
    import numpy as np
    N = 2
    for Product, category_id in sorted(category_to_id.items()):
      features_chi2 = chi2(features, labels == category_id)
      indices = np.argsort(features_chi2[0])
      feature_names = np.array(tfidf.get_feature_names())[indices]
      unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
      bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
      print("# '{}':".format(Product))
      print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
      print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))
