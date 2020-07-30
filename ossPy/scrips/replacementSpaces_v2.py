#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 17:56:52 2020

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
    
    allNoSpaceSymbol=pd.DataFrame(inputColumn[inputColumnName[0]].str.replace('[^a-zA-Z0-9]',''))
    
    tableUniqueFullNameCounts['remapping']=''
    
    #get the remaping to users
    sortedInputColumn, sortedTableUniqueFullNameCounts=ossPyFuncs.uniquePandasIndexMapping(inputColumn)
    
    
    #iterate across entries with guesses
    for index, row in tableUniqueFullNameCounts.iterrows():
            #because our entries are sorted by frequency we can safely assume
            #that the fist time we encounter a nospacesymbol variant of a substring
            #we are also encountering its most frequent form.  As such, it is safe
            #for us to use this most frequent version to replace less frequent versions.
            #Further more, we can remove less frequent substring variants from consideration.
            #This ideally speeds up our computations as there are less entries to check against
        
            #set current entry number
            currentEntry=tableUniqueFullNameCounts[inputColumnName[0]].loc[index]
            
            #get the lowercase form of it
            #currentLower=currentEntry.lower()
            #extract current string from company vector
            #DID YOU KNOW that underscore counts as a letter character with \W ?
            currentNoSpaceOrSymbol=re.sub('[^a-zA-Z0-9]','',currentEntry)
            #if that's not empty
            if len(currentNoSpaceOrSymbol)>0:
                #remove leading white space, just in case this is an entry that has been deleted from
                currentEntry=re.sub('^[ \\t]+','',currentEntry)
                currentEntry=re.compile(currentEntry)
                #make replacement to the noSpaceSymbol vector
                allNoSpaceSymbol=pd.DataFrame(allNoSpaceSymbol[inputColumnName[0]].str.replace('(?i)\\b'+currentNoSpaceOrSymbol+'(?i)\\b',currentEntry))
                #find the unique name indexes these correspond to
                noSpaceSymbolMatches=uniqueNoSpaceSymbol[inputColumnName[0]].str.contains('(?i)\\b'+currentNoSpaceOrSymbol+'\\b')
                #get the names this corresponds to
                toRemoveEntries=pd.DataFrame(tableUniqueFullNameCounts[inputColumnName[0]].loc[noSpaceSymbolMatches])
                #iteratively remove it from the unique list
                for index, row in toRemoveEntries.iterrows():
                    #some of the to remove terms have regex features.  We need to compile them to prevent this from causing problems
                    currentToRemove=re.compile(toRemoveEntries[inputColumnName[0]].loc[index])
                    #perform the deletion
                    tableUniqueFullNameCounts=pd.DataFrame(tableUniqueFullNameCounts[inputColumnName[0]].str.replace('\\b'+currentToRemove+'(?i)\\b',''))
    
    #create an unchanged noSpaceSymbol frame   
    #I guess we dont need this?             
    #noSpaceSymbolCheckFrame=pd.DataFrame(tableUniqueFullNameCounts[inputColumnName[0]].str.replace('[^a-zA-Z0-9]',''))
    #check and see if the entry has been changed from this form.  In such cases
    #we can assume that its origional form was not equivalent to its No Space Form
    #I guess we dont need this?
    #NoSpaceUnchanged=allNoSpaceSymbol.eq(noSpaceSymbolCheckFrame)
    #check and see if the entry has been changed from its origional input
    #In such cases that it has changed, we can assume the new form is the correct one,
    #or that the origional form was the correct one.
    inputUnchanged=allNoSpaceSymbol.eq(inputColumn)
    #also identify Empty listings
    emptyListings=allNoSpaceSymbol[inputColumnName[0]].str.len().fillna(value=0)==0
    #now we alter the input colum to reflect these new values
    inputColumn[inputColumnName[0]].loc[inputColumn]=allNoSpaceSymbol.loc[inputColumn]

    #we have to use sum, because empty is not zero, and is thus non zero, and so np.count_nonzero won't work
    print(str(np.sum(np.logical_and(~inputUnchanged[inputColumnName[0]],  ~emptyListings)))+' entries changed')       
    return inputColumn