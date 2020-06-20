#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 08:16:24 2020

@author: dnb3k
"""
from ossPy import queryToPDTable
import numpy as np
import pandas as pd

postgreSql_selectQuery="SELECT login, company FROM gh.ctrs_raw ;"

result=queryToPDTable(postgreSql_selectQuery)

companyCounts=result['company'].value_counts()

binVals=np.asarray([0,1,5,10,20,50,100,200,np.max(companyCounts)])

binSum=np.zeros([len(binVals)-1,1])
for iBins in range(len(binVals)-1):
    binSum[iBins]=sum(companyCounts[np.logical_and(companyCounts>binVals[iBins],companyCounts<=binVals[iBins+1])])
    
binNames=['1 ','2-5 ','6-10 ','11-20 ','21-50 ','51-100 ','101-200 ', '>201']

import seaborn as sns

workplaceSizeTable=pd.DataFrame(columns=["same workplace","Number of Persons"])
workplaceSizeTable['Number of Persons']=np.squeeze(binSum)
workplaceSizeTable['same workplace']=np.squeeze(binNames)

sns.catplot(data=workplaceSizeTable, kind="bar", x='same workplace',y='Number of Persons', palette='Spectral');

