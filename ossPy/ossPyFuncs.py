#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 12:57:42 2020

@author: dnb3k
"""

def queryToPDTable(postgreSql_selectQuery):
    """Return the output of a SDAD mysql query as a table
    
    Keyword arguments:
    postgreSql_selectQuery -- a properly formatted mysql query
   
    """

    import os
    import psycopg2
    import pandas as pd

    #basic query function to the database using environmental variables for
    #the user name and password
    conn=psycopg2.connect(host="postgis1",
                      dbname="sdad",
                      user=os.environ.get('UVA_uname'),
                      password=os.environ.get('UVA_pass'))

    #convert it to a pandas dataframe
    dataOut=pd.read_sql_query(postgreSql_selectQuery,conn)

    return dataOut

def composeWorkplaceOntology():
    """Create a table featuring valid workplace institutions
    """

    import ossPyFuncs 
    import pandas as pd
    
    #mysql query to extract full table from government organizations
    #certian table columns feature capital letters which cases uproblems
    postgreSql_selectQuery="SELECT * FROM us_gov_manual.us_govman_2019 ;"
    #pass querry and obtain table
    govTable=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

    #mysql query to obtain academic instutions
    postgreSql_selectQuery="SELECT institution FROM hipolabs.universities ;"
    #pass querry and obtain table
    univTable=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)
    
    postgreSql_selectQuery="SELECT company FROM forbes.fortune2018_us1000;"
    businesses1=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)
    
    postgreSql_selectQuery="SELECT company FROM forbes.fortune2019_us1000;"
    businesses2=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)
    
    postgreSql_selectQuery="SELECT company FROM forbes.fortune2020_global2000;"
    businesses3=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

    #combine theinsitutions into a vector
    combinedSeries=[govTable['AgencyName'],univTable['institution'],businesses1['company'],businesses2['company'],businesses3['company']]
    #turn the multi item vector into a single series
    fullWordbank=pd.concat(combinedSeries)
    #turn that series into a pd dataframe
    wordbankTable=pd.DataFrame(fullWordbank.unique())

    return wordbankTable

def checkColumnMapping(inputRawColumn,targetOntology):
    """Assess which unique entries in an input column are in target ontology
    
    Keyword arguments:
    inputRawColumn -- a single column from a pandas table featuring potentially
    non-unique entries 
    
    targetOntology -- a single column from a pandas table featuring only unique
    entries.  Values from [inputRawColumn] will be assessed against this column
    """
    
    import pandas as pd
    import numpy as np

    #extract counts of unique values from input column
    columnUniqueCounts=inputRawColumn.iloc[:,0].value_counts()
    #convert that output to a proper table
    tableUniqueCounts=columnUniqueCounts.reset_index()
    
    #obtain a boolean vector which indicates the presence of terms from
    #inputRawColumn in targetOntology
    presentBoolVec=np.in1d(tableUniqueCounts.index,targetOntology)
    #set the boolean vector as a column of the output
    tableUniqueCounts['present']=presentBoolVec
    tableUniqueCounts.rename(columns={tableUniqueCounts.columns[0]:tableUniqueCounts.columns[1],tableUniqueCounts.columns[1]:"count"},inplace=True)
    
    return tableUniqueCounts

def eraseFromColumn(inputColumn,eraseList):
   """iteratively delete regex query matches from input list
    
    Keyword arguments:
    inputColumn -- a column from a pandas dataframe, this will be the set of
    target words/entries that deletions will be made from
    eraseList -- a column containing strings (regex expressions) which will be
    deleted from the inputColumn, in an iterative fashion
    """
    
   import pandas as pd
   import re
   
   eraseList['changeNum']=0
   eraseList['changeIndexes']=''
   
   #necessary, due to escape nonsense
   inputColumn=inputColumn.replace(regex=True, to_replace='\\\\',value='/')
     
   for index, row in eraseList.iterrows():
       
       curReplaceVal=row[0]
       currentRegexExpression=re.compile(curReplaceVal)
       CurrentBoolVec=inputColumn.str.contains(currentRegexExpression,na=False)
       eraseList['changeIndexes'].iloc[index]=[i for i, x in enumerate(CurrentBoolVec) if x]
       eraseList['changeNum'].iloc[index]=len(eraseList['changeIndexes'].iloc[index])
       inputColumn.replace(regex=True, to_replace=currentRegexExpression,value='', inplace=True)

   return inputColumn, eraseList;

def expandFromColumn(inputColumn,replaceList):
   """iteratively replace regex query matches from input list
    
    Keyword arguments:
    inputColumn -- a column from a pandas dataframe, this will be the set of
    target words/entries that replacements will be made to
    replaceList -- a two column (pandas) object.  The first column containing strings 
    (regex expressions) which will be
    replaced  by the entry (from the same row) from the second column, in an iterative fashion
    """
    
   import pandas as pd
   import re
   
   #necessary, due to escape nonsense
   inputColumn=inputColumn.replace(regex=True, to_replace='\\\\',value='/')
   
   replaceList['changeNum']=0
   replaceList['changeIndexes']=''

   for index, row in replaceList.iterrows():
       curReplaceVal=row[0]
       currentRegexExpression=re.compile(curReplaceVal)
       CurrentBoolVec=inputColumn.str.contains(currentRegexExpression,na=False)
       replaceList['changeIndexes'].iloc[index]=[i for i, x in enumerate(CurrentBoolVec) if x]
       replaceList['changeNum'].iloc[index]=len(replaceList['changeIndexes'].iloc[index])
       inputColumn=inputColumn.replace(regex=True, to_replace=currentRegexExpression,value=row[1])
   return inputColumn, replaceList;

def uniquePandasIndexMapping(inputColumn):
    """quickly mapps the unique name entries back to input entries
    
    Keyword arguments:
    inputDataToAssess -- a SINGLE column from a pandas dataframe, presumably with 
    duplications.  Will create a frequency table and a mapping back to the source entries.
    """
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
        sortedTableUniqueFullNameCounts['inputIndexMapping'].iloc[index]=sortedInputColumn['userIndex'].iloc[currentRange].array
        currentSum=currentSum+sortedTableUniqueFullNameCounts['count'].iloc[index]

    return sortedInputColumn, sortedTableUniqueFullNameCounts;

def addBooleanColumnFromCriteria(inputDataToAssess,assessItems,newColumnName):
    """iteratively determine if input column contains member of other column
    
    Keyword arguments:
    inputDataToAssess -- a SINGLE column from a pandas dataframe, this will be the set of
    target words/entries that deletions will be made from
    assessItems -- a seriers or dataframe containing strings
    (regex expressions) which will be searched for (as substrings)
    in the inputDataToAssess.  This will be done in an iterative fashion, and
    a bolean vector will be created and appended to the output, indicating
    which entries in inputDataToAssess contained a substring from assessItems.
    newColumnName -- name of the new column (i.e. 'government', 'academic', etc.)
    """
    
    import pandas as pd
    import re
   
    inputDataToAssess[newColumnName]=False
   
    #necessary, due to escape nonsense
    inputDataToAssess=inputDataToAssess.replace(regex=True, to_replace='\\\\',value='/')
     
    for index, row in assessItems.iterrows():
       
       curReplaceVal=row[0]
       currentRegexExpression=re.compile(curReplaceVal)
       CurrentBoolVec=inputDataToAssess[inputDataToAssess.columns[0]].str.contains(currentRegexExpression,na=False)
       inputDataToAssess[newColumnName].loc[CurrentBoolVec]=True

    return inputDataToAssess;

def iterativeFullFuzzyMatch(inputColumn):
    """iteratively perform a fuzzy match on entire input column
    
    Keyword arguments:
    inputColumn -- a SINGLE column from a pandas dataframe, this will be the set of
    target words/entries will be iteratively matched against (except self) seeking
    close matches
    """
    #get the input column names
    inputColumnName=inputColumn.columns
    #get the unique values (and counts)
    tableUniqueFullNameCounts=inputColumn[inputColumnName[0]].value_counts()
    #convert that output to a proper table
    tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()
    #rename the columns
    tableUniqueFullNameCounts.rename(columns={inputColumnName[0]:"count","index":inputColumnName[0]},inplace=True)

    import difflib
    import numpy as np
    
    #create blank column
    tableUniqueFullNameCounts['guesses']=''

    for index, row in tableUniqueFullNameCounts.iterrows():
       blankBool=np.full((len(tableUniqueFullNameCounts.index)),True)
       curBool=blankBool
       curBool[index]=False
       currentChecklist=tableUniqueFullNameCounts[inputColumnName[0]].loc[curBool]
       tableUniqueFullNameCounts['guesses'].loc[index]=difflib.get_close_matches(tableUniqueFullNameCounts[inputColumnName[0]].loc[index],currentChecklist,cutoff=0.8)
    
    return tableUniqueFullNameCounts

def createSubstringMatrix(inputColumn):
    """iteratively perform substring assesment across all entries and map these 
    relations into a directed matrix
    Keyword arguments:
    inputColumn -- a SINGLE column from a pandas dataframe, this will be the set of
    target words/entries will be iterated over when performing the substring matching
    NOTE: The returned matrix is in a strange format and mary require converstion to
    interact with
    """
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

    import scipy.sparse as sparse
    import re

    #create a sparse matrix of appropriate dimensions
    substringMatrix=sparse.coo_matrix((len(tableUniqueFullNameCounts.index),len(tableUniqueFullNameCounts.index)),dtype=bool)

    #convert to format the permits modification
    accessibleMatrix=substringMatrix.tolil()

    #iterate acroos unique listings
    for index, row in tableUniqueFullNameCounts.iterrows():
    
        #formulate a good regex expression
        currentRegex=re.compile('(?i)\\b'+re.escape(tableUniqueFullNameCounts[inputColumnName[0]].loc[index])+'\\b')
        #print(currentRegex)
        #get all company listings that feature the current company string
        currentBool=tableUniqueFullNameCounts[inputColumnName[0]].str.contains(currentRegex)
    
        #fill in boolean values
        accessibleMatrix[index,:]=currentBool
    
    return tableUniqueFullNameCounts, accessibleMatrix

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