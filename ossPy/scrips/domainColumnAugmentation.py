#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:01:46 2020

@author: dnb3k
"""

#use the unique Full Tokens code to get teh dataframe
import ossPyFuncs
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt
import os
import numpy as np


#perform sql query to get company column
postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

#obtain the eralse list
currentDir=os.path.dirname('ossPyFuncs.py')
eraseList=pd.read_csv(os.path.join(currentDir,'keyFiles/eraseStrings_v6.csv'),quotechar="'")
#apply the erase list
semiCleanedOutput=pd.DataFrame(ossPyFuncs.eraseFromColumn(inputRaw['company'],eraseList))

#get the counts for the unique values
tableUniqueFullNameCounts=semiCleanedOutput.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()

#rename the columns
tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)

selfEmployedKeys=re.compile('(?i)self|Me, myself and I|personal|^home$|private|individual|myself|^me$|\\bindependent\\b|independent contractor|consultant|freelancer|freelance|self-employed| my ')


dataTest2=tableUniqueFullNameCounts[tableUniqueFullNameCounts['company'].str.contains(selfEmployedKeys)]
dataTest2=tableUniqueFullNameCounts[tableUniqueFullNameCounts['company'].str.contains('(?i)S\.R\.L\.')]

freelanceSum=np.sum(dataTest2['count'])
allSum=np.sum(tableUniqueFullNameCounts['count'])