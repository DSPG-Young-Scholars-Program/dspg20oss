#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:50:59 2020

@author: dnb3k
"""

import ossPyFuncs
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt

    
#perform sql query to get company column
postgreSql_selectQuery="SELECT login, company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

#get the sorted company count
gitWorkplaceCounts=inputRaw['company'].value_counts()
#reset the columns
gitWorkplaceCounts=gitWorkplaceCounts.reset_index()

testColumn=inputRaw['company']
longString=testColumn.str.cat(sep=' ')
longStringSeparated=longString.split(' ')

uniqueTokenComponentsFrame=pd.DataFrame(longStringSeparated)

columnUniqueCounts=uniqueTokenComponentsFrame.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueCounts=columnUniqueCounts.reset_index()

