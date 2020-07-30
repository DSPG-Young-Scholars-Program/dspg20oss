#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:46:45 2020

@author: dnb3k
"""
def spaceSymbolRemap(inputColumn):
    """remapps entries with same space and symbol free string to most common element
    
    Keyword arguments:
    inputColumn -- a column from a pandas dataframe, presumably with duplicate 
    entires, as frequency will guide this process.
    space/symbol/case variants of the same string will be remapped to most common element
    """
    import pandas as pd
    import re
    import numpy as np
    import ossPyFuncs
    
    #get the input column names
    inputColumnName=inputColumn.columns
    
    #get the unique values (and counts)
    tableUniqueFullNameCounts=inputColumn[inputColumnName[0]].value_counts()
    #convert that output to a proper table
    tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()
    #rename the columns
    tableUniqueFullNameCounts.rename(columns={inputColumnName[0]:"count","index":inputColumnName[0]},inplace=True)

    tableUniqueFullNameCounts=tableUniqueFullNameCounts.sort_values(by=['count',inputColumnName[0]],ascending=[False,False])

    tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index(drop=True)
    
    uniqueNoSpaceSymbol=pd.DataFrame(tableUniqueFullNameCounts[inputColumnName[0]].str.replace('[^a-zA-Z0-9]',''))
    
    tableUniqueFullNameCounts['remapping']=''
#iterate across entries with guesses
    for index, row in tableUniqueFullNameCounts.iterrows():
            #set current entry number
            currentEntry=tableUniqueFullNameCounts[inputColumnName[0]].loc[index]
            #get the lowercase form of it
            #currentLower=currentEntry.lower()
            #extract current string from company vector
            currentNoSpaceOrSymbol=re.sub('\\W','',currentEntry)
            #extract what may be a list of guesses
            noSpaceSymbolMatches=uniqueNoSpaceSymbol[inputColumnName[0]].str.contains('(?i)\\b'+currentNoSpaceOrSymbol+'\\b')
            #find the counts of the entires that match up with this, use the wisdom of the crowds
            currentCounts=tableUniqueFullNameCounts['count'].loc[noSpaceSymbolMatches]
            #find the listing of the label with the max frequency
            #make an array of it
            indexFrame=currentCounts.reset_index()
            #find the index
            currentIndex=indexFrame.loc[(indexFrame['count']==np.max(currentCounts))]
            if (not index==currentIndex['index'].iloc[0]) and len(currentNoSpaceOrSymbol)>0:
                #extract the name that is to be remapped to
                mappedName=tableUniqueFullNameCounts[inputColumnName[0]].loc[currentIndex['index'].iloc[0]]
                #place it in the table
                tableUniqueFullNameCounts.at[index,'remapping']=mappedName
            
            print('Remaping identification complete')

    #find where you need to perform regex replacements
    remapPresent=tableUniqueFullNameCounts['remapping'].str.len()>0

    #create subtable for things to replace
    replacementSubtable=tableUniqueFullNameCounts.loc[remapPresent]

    #use the replacement function to replace the relevant items
    fixedList,fixedReport=ossPyFuncs.expandFromColumn(inputColumn,pd.DataFrame(replacementSubtable['company','remapping']))

    print('remapping complete')
    return fixedList, fixedReport
