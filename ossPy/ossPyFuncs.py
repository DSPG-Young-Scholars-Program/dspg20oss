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

    #combine theinsitutions into a vector
    combinedSeries=[govTable['AgencyName'],univTable['institution']]
    #turn the multi item vector into a single series
    fullWordbank=pd.concat(combinedSeries)
    #turn that series into a pd dataframe
    wordbankTable=pd.DataFrame(fullWordbank)

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

   for index, row in eraseList.iterrows():
       print(row[0])
       curReplaceVal=row[0]
       currentRegexExpression=re.compile(curReplaceVal)
        
    
       holdColumn=inputColumn.replace(regex=True, to_replace=currentRegexExpression,value='')
       tabulationTable=inputColumn.eq(holdColumn).value_counts()
       tabulationTable
       print(str(inputColumn.size-tabulationTable.loc[True])+ " items changed")
       inputColumn=holdColumn
   return inputColumn

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

   for index, row in replaceList.iterrows():
       print(row[0])
       curReplaceVal=row[0]
       currentRegexExpression=re.compile(curReplaceVal)
        
    
       holdColumn=inputColumn.replace(regex=True, to_replace=currentRegexExpression,value=row[1])
       tabulationTable=inputColumn.eq(holdColumn).value_counts()
       tabulationTable
       print(str(inputColumn.size-tabulationTable.loc[True])+ " items changed")
       inputColumn=holdColumn
   return inputColumn
