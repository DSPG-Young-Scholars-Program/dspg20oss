#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:39:33 2020

@author: dnb3k
"""
import ossPyFuncs
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import sparse
import scipy
import sys
tableUniqueFullNameCounts=pd.read_csv('/home/dnb3k/Documents/PackageOuts/inOutDegree.csv')
sparseMatrixHold=scipy.sparse.load_npz('/home/dnb3k/Documents/PackageOuts/matrix.npz')

tableUniqueFullNameCounts.to_csv('/home/dnb3k/Documents/PackageOuts/ratioIndegree.csv')


tableUniqueFullNameCounts['reachability']=''
tableUniqueFullNameCounts['maxReachable']=0



for index, row in tableUniqueFullNameCounts.iterrows():
    
    nodeArray =scipy.sparse.csgraph.depth_first_order(sparseMatrixHold,index,return_predecessors=False)
    
   # tableUniqueFullNameCounts['reachability'].loc[index]=nodeArray
    tableUniqueFullNameCounts['maxReachable'].loc[index]=np.min(nodeArray)
    
tableUniqueFullNameCounts['maxMatch']=tableUniqueFullNameCounts['maxReachable']==tableUniqueFullNameCounts['Unnamed: 0']
tableUniqueFullNameCounts['countInDegreeRatio']=np.divide(tableUniqueFullNameCounts['count'],tableUniqueFullNameCounts['indegree'])

tableUniqueFullNameCounts.to_csv('/home/dnb3k/Documents/PackageOuts/maxMatch.csv')   

tableUniqueFullNameCounts['deadEnds']=''

deadEndIndexes=np.where(tableUniqueFullNameCounts['outdegree']==1)[0]

for index, row in tableUniqueFullNameCounts.iterrows():
    
    nodeArray =scipy.sparse.csgraph.depth_first_order(sparseMatrixHold,index,return_predecessors=False)
    
    currDeadEnds=np.intersect1d(nodeArray,deadEndIndexes)
    
   # tableUniqueFullNameCounts['reachability'].loc[index]=nodeArray
    tableUniqueFullNameCounts['deadEnds'].loc[index]=currDeadEnds

