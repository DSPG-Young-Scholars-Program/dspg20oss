#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 21:11:53 2020



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

tableUniqueFullNameCounts=semiCleanedOutput.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()

#rename the columns
tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)

#create some new columns
tableUniqueFullNameCounts['guesses']=''
tableUniqueFullNameCounts['additionalIndividuals']=''

#iterate acroos unique listings
for iAttempts in range(len(tableUniqueFullNameCounts.index)):
    #get all company listings that feature the current company string
    currentBool=tableUniqueFullNameCounts['company'].str.contains( tableUniqueFullNameCounts['company'].iloc[iAttempts])
    #get teh indexes associated with those names
    currentIndexes=currentBool[currentBool].index
    #find the number of additional individuals that are found with
    #the regex search
    currentAdditionalIndividuals=np.sum(tableUniqueFullNameCounts['count'].iloc[currentIndexes])-tableUniqueFullNameCounts['count'].iloc[iAttempts]
    #resort the indexes such that the first listing has the
    #most number of employees associated with it
    currentGeusses= tableUniqueFullNameCounts['company'].loc[currentIndexes.sort_values()]
    #create a full string vector of these company names, and place it in the new column
    tableUniqueFullNameCounts['guesses'].iloc[iAttempts]= currentGeusses.str.cat(sep=' /// ')
    #place the additional sum in its new column
    tableUniqueFullNameCounts['additionalIndividuals'].iloc[iAttempts]= currentAdditionalIndividuals