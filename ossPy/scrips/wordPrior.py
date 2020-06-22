#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:50:59 2020
this script generates a table containing the unique sub-tokens (i.e. 
individual words) found in workplace names

@author: dnb3k
"""

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
eraseList=pd.read_csv(os.path.join(currentDir,'keyFiles/eraseStrings.csv'),quotechar="'")
#apply the erase list
semiCleanedOutput=pd.DataFrame(ossPyFuncs.eraseFromColumn(inputRaw['company'],eraseList))

#cat together all user's workplace names (note, we are not applying unique first)
longString=semiCleanedOutput['company'].str.cat(sep=' ')

#separate each word into a extremely long list
longStringSeparated=longString.split(' ')

#turn it into a dataframe
uniqueSubTokenFrame=pd.DataFrame(longStringSeparated)

#get the count on that column
columnUniqueCounts=uniqueSubTokenFrame.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueCounts=columnUniqueCounts.reset_index()
tableUniqueCounts.rename(columns={0:"count","index":"token"},inplace=True)