#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 08:56:01 2018

@author: crazytrau
"""

# import library
import json
import csv
import numpy as np

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
    numTweet=0
    numLabel=[0,0,0,0]

    #read every trending and export json file
    with open('../../data/TT-annotations.csv', newline='', encoding="utf8") as csvfile:
        trendingTopicArr = csv.reader(csvfile, delimiter=';')
        for trendingTopic in trendingTopicArr:
            path='../../../features/'+trendingTopic[0]+'.json'
            data = json.load(open(path))
            numberItem = len(data)
            numTweet+= numberItem
            if numberItem > 0 :
                numLabel[toLabel(trendingTopic[3])]+=1
            else:
                print (trendingTopic[0], toLabel(trendingTopic[3]))
    print(numTweet, numLabel)
