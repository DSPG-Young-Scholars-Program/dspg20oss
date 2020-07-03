#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 19:23:14 2020
This code splits the input table into a table corresponding to those companies
that have more than the parameter setting (coworkerThreshold) number of
employees and those companies that have fewer.


@author: dnb3k
"""


#this is a paramter that we set to split the dataframe into the "upper half"
#and the "lower half"
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

#obtain the erase list
currentDir=os.path.dirname('ossPyFuncs.py')
eraseList=pd.read_csv(os.path.join(currentDir,'keyFiles/eraseStrings_v6.csv'),quotechar="'")
#apply the erase list
semiCleanedOutput=pd.DataFrame(ossPyFuncs.eraseFromColumn(inputRaw['company'],eraseList))

#get the unique counts of the column
tableUniqueFullNameCounts=semiCleanedOutput.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()

#rename the columns
tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)

#apply the less than and greater than logical operations
multiCoWorkerTable=dataTest2=tableUniqueFullNameCounts[tableUniqueFullNameCounts['count'].ge(coworkerThreshold)]
singletonTable=dataTest2=tableUniqueFullNameCounts[tableUniqueFullNameCounts['count'].lt(coworkerThreshold)]