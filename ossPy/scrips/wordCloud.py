#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:50:59 2020
This function creates a word cloud for the compnay column after cleanining 
those names.  Saves the output down as a svg


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
eraseList=pd.read_csv(os.path.join(currentDir,'keyFiles/eraseStrings_v6.csv'),quotechar="'")
#apply the erase list
semiCleanedOutput=ossPyFuncs.eraseFromColumn(lowerInput['company'],eraseList)

#replace interior spaces and periods (which the wordcloud splits at)
spacesReplaced=semiCleanedOutput.str.replace(' ','_')
periodsReplaced=spacesReplaced.str.replace('\.','_')


#turn that output into a long string
longString=periodsReplaced.str.cat(sep=' ')

#generate a wordcloud and convert it to svg
outcloud=wordcloud.WordCloud(width=2000, height=1000, max_words=2000).generate(longString)
svgCloud=outcloud.to_svg()

#save it down as an svg
svgOut=open(os.path.join(currentDir,'figures/wordcloud.svg'),"w")
svgOut.write(svgCloud)
svgOut.close()