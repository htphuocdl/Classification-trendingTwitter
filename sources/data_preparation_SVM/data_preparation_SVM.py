#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 19:56:36 2018

@author: crazytrau
"""
# import library
import csv
import sys
sys.path.insert(0, '../Features/')
from getData import getDataHashCode

#main function
if __name__ == '__main__':
    # main variable
    trendingTopicArr=[]
    #read every trending and export json file
    with open('../../data/TT-annotations.csv', newline='') as csvfile:
        trendingTopicArr = csv.reader(csvfile, delimiter=';')
        for trendingTopic in trendingTopicArr:
            getDataHashCode(trendingTopic[0])