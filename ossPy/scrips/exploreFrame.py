#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:39:44 2020
This code is useful for exploring a dataframe, towards the end you can search
the name column for companies featuring a specific string


@author: dnb3k
"""

import ossPyFuncs
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt
import os
import nltk

 #perform sql query to get company column
postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)


currentDir=os.path.dirname('ossPyFuncs.py')
replaceList=pd.read_csv(os.path.join(currentDir,'keyFiles/expandAbrevs.csv'),quotechar="'",header=None)
inputColumn, replaceList=ossPyFuncs.expandFromColumn(inputRaw['company'],replaceList)

#obtain the eralse list
currentDir=os.path.dirname('ossPyFuncs.py')
eraseList=pd.read_csv(os.path.join(currentDir,'keyFiles/eraseStrings_v6.csv'),quotechar="'",header=None)
#apply the erase list
semiCleanedOutput=pd.DataFrame(ossPyFuncs.eraseFromColumn(inputRaw['company'],eraseList))

#cat together all user's workplace names (note, we are not applying unique first)
longString=inputRaw['company'].str.cat(sep=' ')

#separate each word into a extremely long list
longStringSeparated=longString.split(' ')

#turn it into a dataframe
uniqueSubTokenFrame=pd.DataFrame(longStringSeparated)

#get the count on that column
columnUniqueCounts=uniqueSubTokenFrame.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueCounts=columnUniqueCounts.reset_index()
#reset the names
tableUniqueCounts.rename(columns={0:"count","index":"token"},inplace=True)

#now for unique full names
tableUniqueFullNameCounts=inputRaw.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()

#rename the columns
tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)
tableUniqueFullNameCounts=tableUniqueFullNameCounts[~tableUniqueFullNameCounts['company'].str.contains("^$")]

[^a-zA-Z\d\s:]
#perform a regex search
dataTest1=tableUniqueCounts[tableUniqueCounts['com'].str.contains("[^a-zA-Z\-@\.\,\\d\\s:]")]
dataTest1=tableUniqueCounts[tableUniqueCounts['token'].str.contains("href")]
dataTest2=tableUniqueCounts2[tableUniqueCounts2['token'].str.contains("\.")]

dataTest3=tableUniqueFullNameCounts[tableUniqueFullNameCounts['company'].str.contains("Argonne")]

dataTest3=tableUniqueCounts[tableUniqueCounts['token'].str.contains("^\\W+?$")]


#word bigrams
wordTokens=nltk.word_tokenize(longString)

wordBigrams=nltk.bigrams(wordTokens)
fdist=nltk.FreqDist(wordBigrams)