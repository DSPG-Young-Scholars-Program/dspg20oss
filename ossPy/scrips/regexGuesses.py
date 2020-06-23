#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 21:11:53 2020
This script iterates across unique listings in the workplace association
column and performs a "string contains" operation on that term to return
all those other workplaces which feature this string.  In a sense, this relies
on a "wisdom of crowds" and "lowest common denominator" effect, such that
(1) its safe to assume that the most commonly listed workplace names are 
accurately spelled and the most viable label for that company and (2) that 
it constitutes the shortest common string associated with that company, because
probabalistically, the conjunct probabability of adding more words to a 
comany name listing results in longer names being less common. As such, the
shorter names will be higher in this list and more common.


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