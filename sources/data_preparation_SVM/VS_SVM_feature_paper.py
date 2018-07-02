#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 17:53:04 2018

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
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Importing the dataset
    dataset = pd.DataFrame(arrVectors, columns=columns)
    X = dataset.iloc[:,0:-1].values
    y = dataset.iloc[:, 14].values
    
    import numpy as np
    print(dataset.groupby('class').size())
    abc = pd.DataFrame(np.array(dataset.groupby('class').size()), index=['ongoing-event','news','meme','commemorative'])
    my_colors = 'rgbkymc'
    abc.plot.bar(color=my_colors)
    plt.show()
    
    from sklearn.model_selection import cross_val_score
    from sklearn.svm import SVC
    models = [
        SVC(kernel="linear"),
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