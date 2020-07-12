#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:54:54 2020

@author: dnb3k
"""

import ossPyFuncs
import pandas as pd
import wordcloud
import re
import matplotlib.pyplot as plt
import os
import numpy as np


postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

currentDir=os.path.dirname('ossPyFuncs.py')
houseHoldList=pd.read_csv(os.path.join(currentDir,'keyFiles/individualKeys.csv'),quotechar="'",header=None)

outColumn=ossPyFuncs.addBooleanColumnFromCriteria(inputRaw,houseHoldList,'household')

np.count_nonzero(outColumn['household'])


#iteratively apply the list as a string search, and mark true where a match is found
householdOutColumn=ossPyFuncs.addBooleanColumnFromCriteria(inputRaw,houseHoldList,'household')

print(str(np.count_nonzero(householdOutColumn['household'])) + ' household innovators found')

subsetHouseholdUsers=householdOutColumn[householdOutColumn['household']]
subsetHouseholdUsersCountDF=subsetHouseholdUsers['company'].value_counts()
subsetHouseholdUsersCountDF.head(20)