#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 19:56:36 2018

@author: crazytrau
"""
# import library
import json
import csv
from getData import getDataHashCode

#main function
if __name__ == '__main__':
    # main variable
    trendingTopicArr=[]

    data = json.load(open('output.json'))

    toCur = False

    #read every trending and export json file
    with open('../../data/TT-annotations.csv', newline='', encoding="utf8") as csvfile:
        trendingTopicArr = csv.reader(csvfile, delimiter=';')
        for trendingTopic in trendingTopicArr:
            print (trendingTopic[0], data)
            if (toCur == True):
                num = getDataHashCode(trendingTopic[0])
            if (trendingTopic[0] == data):
                toCur = True
