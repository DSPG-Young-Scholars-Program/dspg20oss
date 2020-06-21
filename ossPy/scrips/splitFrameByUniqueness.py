#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 19:23:14 2020

@author: dnb3k
"""



coworkerThreshold=2

import ossPyFuncs
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt
import os

#perform sql query to get company column
postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

#obtain the eralse list
currentDir=os.path.dirname('ossPyFuncs.py')
eraseList=pd.read_csv(os.path.join(currentDir,'keyFiles/eraseStrings_v6.csv'),quotechar="'")
#apply the erase list
semiCleanedOutput=pd.DataFrame(ossPyFuncs.eraseFromColumn(inputRaw['company'],eraseList))

tableUniqueFullNameCounts=semiCleanedOutput.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()

#rename the columns
tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)

multiCoWorkerTable=dataTest2=tableUniqueFullNameCounts[tableUniqueFullNameCounts['count'].ge(2)]
singletonTable=dataTest2=tableUniqueFullNameCounts[tableUniqueFullNameCounts['count'].lt(2)]

longString=singletonTable['company'].str.cat(sep=' ')

#separate each word into a extremely long list
longStringSeparated=longString.split(' ')

#turn it into a dataframe
uniqueSubTokenFrame=pd.DataFrame(longStringSeparated)

#get the count on that column
columnUniqueCounts=uniqueSubTokenFrame.iloc[:,0].value_counts()
#convert that output to a proper table
SingletontableUniqueCounts=columnUniqueCounts.reset_index()
SingletontableUniqueCounts.rename(columns={0:"count","index":"token"},inplace=True)


longString=multiCoWorkerTable['company'].str.cat(sep=' ')

#separate each word into a extremely long list
longStringSeparated=longString.split(' ')

#turn it into a dataframe
uniqueSubTokenFrame=pd.DataFrame(longStringSeparated)

#get the count on that column
columnUniqueCounts=uniqueSubTokenFrame.iloc[:,0].value_counts()
#convert that output to a proper table
MultitableUniqueCounts=columnUniqueCounts.reset_index()
MultitableUniqueCounts.rename(columns={0:"count","index":"token"},inplace=True)