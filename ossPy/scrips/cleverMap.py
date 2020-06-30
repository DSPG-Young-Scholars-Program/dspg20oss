#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:00:22 2020

@author: dnb3k
"""

inputColumn.dropna( inplace=True)

def uniquePandasIndexMapping(inputColumn):
    import numpy as np
    
    
    inputColumn.sort_values(by=['company'], inplace=True)
    sortedInputColumn=inputColumn.reset_index() 
    sortedInputColumn.rename(columns={"index":"userIndex"},inplace=True)
    
    tableUniqueFullNameCounts=inputColumn.iloc[:,0].value_counts()  
    tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index() 
    tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)
    
    tableUniqueFullNameCounts.sort_values(by=['company'], inplace=True)
    sortedTableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()
    sortedTableUniqueFullNameCounts['inputIndexMapping']=''
    
    currentSum=0
    for index, row in sortedTableUniqueFullNameCounts.iterrows():
        currentRange=np.arange(currentSum,currentSum+sortedTableUniqueFullNameCounts['count'].iloc[index])
        sortedTableUniqueFullNameCounts['inputIndexMapping'].iloc[index]=sortedInputColumn['userIndex'].iloc[currentRange]
        currentSum=currentSum+sortedTableUniqueFullNameCounts['count'].iloc[index]

    return sortedInputColumn, sortedTableUniqueFullNameCounts