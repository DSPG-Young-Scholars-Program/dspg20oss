#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:03:22 2020

@author: dnb3k
"""


import ossPyFuncs
import pandas as pd
import re

    

postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"
inputRawColumn=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

postgreSql_selectQuery="SELECT login, company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

eraseList=pd.read_csv('eraseStrings.csv', quotechar="'",header=None)

for index, row in eraseList.iterrows():
    curReplaceVal=row[0]
    currentRegexExpression=curReplaceVal + '(?i)'
    #print(currentRegexExpression)
    inputRawColumn.replace(regex=currentRegexExpression, value='', inplace=True)


targetOntology=ossPyFuncs.composeWorkplaceOntology()

assessTable=ossPyFuncs.checkColumnMapping(inputRawColumn,targetOntology)

dataTest=assessTable[assessTable['company'].str.contains(",")]

