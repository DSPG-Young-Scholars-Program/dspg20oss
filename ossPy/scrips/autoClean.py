#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:54:55 2020

@author: dnb3k
"""

import ossPyFuncs
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

#perform sql query to get company column
postgreSql_selectQuery="SELECT local_language_abbreviation FROM gleif.legal_entities;"
legalEntitiesRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)
longLine=legalEntitiesRaw['local_language_abbreviation'].str.cat(sep=';')
longLineSeparated=pd.DataFrame(longLine.split(';'))
uniqueFrame=pd.DataFrame(longLineSeparated[0].unique())
#uniqueFrame=pd.DataFrame(uniqueFrame[0][~uniqueFrame[0].str.contains('(?i)^co\.$|^co$')]).reset_index(drop=True)
#uniqueFrame=pd.DataFrame(uniqueFrame[0][~uniqueFrame[0].str.contains('(?i)^co\.$|^co$')]).reset_index(drop=True)

sqlQueryFormattedFrame=pd.DataFrame('(?i)\\b'+uniqueFrame[0].astype(str)+'\\b')

inputColumn, eraseList=ossPyFuncs.eraseFromColumn(inputRaw['company'],sqlQueryFormattedFrame)

eraseList.sort_values(by=['changeNum'],ascending=False,inplace=True)
eraseList.reset_index(drop=True,inplace=True)

longLine=barAbbreviations[0].str.cat(sep='|')




#formulate a good regex expression
currentRegex=re.compile('(?i)\\b'+longLine+'\\b')
    
#get all company listings that feature the current company string
test5=uniqueFrame[uniqueFrame[0].str.contains('(株)\1{9,}')]

#perform sql query to get company column
postgreSql_selectQuery="SELECT domain FROM datahub.domain_names;"
domainsTable=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)
domainsTableFormattedFrame=pd.DataFrame('(?i)\\b'+domainsTable['domain'].astype(str)+'\\b')
inputColumn, eraseList=ossPyFuncs.eraseFromColumn(inputRaw['company'],domainsTableFormattedFrame)
eraseList.sort_values(by=['changeNum'],ascending=False,inplace=True)
eraseList.reset_index(drop=True,inplace=True)

print(str(np.sum(eraseList['changeNum'])) + ' listings changed')

eraseList.head(25)