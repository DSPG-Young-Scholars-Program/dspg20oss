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
   

   for index, row in eraseList.iterrows():
       
       curReplaceVal=row[0]
       currentRegexExpression=re.compile(curReplaceVal)
       CurrentBoolVec=inputColumn.str.contains(currentRegexExpression,na=False)
       eraseList['changeIndexes'].iloc[index]=[i for i, x in enumerate(CurrentBoolVec) if x]
       eraseList['changeNum'].iloc[index]=len(eraseList['changeIndexes'].iloc[index])
       inputColumn.replace(regex=True, to_replace=currentRegexExpression,value='', inplace=True)

   return inputColumn, eraseList;

def expandFromColumn(inputColumn,replaceList):
   """iteratively delete regex query matches from input list
    
    Keyword arguments:
    inputColumn -- a column from a pandas dataframe, this will be the set of
    target words/entries that deletions will be made from
    eraseList -- a column containing strings (regex expressions) which will be
    deleted from the inputColumn, in an iterative fashion
    """
    
   import pandas as pd
   import re

   replaceList['changeNum']=0
   replaceList['changeIndexes']=''

   for index, row in replaceList.iterrows():
       print(row[0])
       curReplaceVal=row[0]
       currentRegexExpression=re.compile(curReplaceVal)
       CurrentBoolVec=inputColumn.str.contains(currentRegexExpression,na=False)
       replaceList['changeIndexes'].iloc[index]=[i for i, x in enumerate(CurrentBoolVec) if x]
       replaceList['changeNum'].iloc[index]=len(replaceList['changeIndexes'].iloc[index])
       inputColumn=inputColumn.replace(regex=True, to_replace=currentRegexExpression,value=row[1])
   return inputColumn, replaceList;

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

    return sortedInputColumn, sortedTableUniqueFullNameCounts;
