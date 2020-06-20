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
import os

#perform sql query to get company column
postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)
#force case insensitivity
lowerInput=pd.DataFrame(inputRaw['company'].str.lower())

#obtain the eralse list
currentDir=os.path.dirname('ossPyFuncs.py')
eraseList=pd.read_csv(os.path.join(currentDir,'keyFiles/eraseStrings.csv'),quotechar="'")
#apply the erase list
semiCleanedOutput=ossPyFuncs.eraseFromColumn(lowerInput['company'],eraseList)

#replace interior spaces
spacesReplaced=semiCleanedOutput.str.replace('\ ','_')

#turn that output into a long string
longString=spacesReplaced.str.cat(sep=' ')

outcloud=wordcloud.WordCloud(max_words=2000).generate(longString)
plt.figure(figsize=(16,32),dpi=200)
plt.imshow(outcloud, interpolation="bilinear")