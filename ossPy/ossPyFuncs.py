#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 12:57:42 2020

@author: dnb3k
"""

def queryToPDTable(postgreSql_selectQuery):
    import os
    import psycopg2
    import pandas as pd

    conn=psycopg2.connect(host="postgis1",
                      dbname="sdad",
                      user=os.environ.get('UVA_uname'),
                      password=os.environ.get('UVA_pass'))

    dataOut=pd.read_sql_query(postgreSql_selectQuery,conn)

    return dataOut




def composeWorkplaceOntology():
    
    import ossPyFuncs 

    import pandas as pd
    postgreSql_selectQuery="SELECT * FROM us_gov_manual.us_govman_2019 ;"

    govTable=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

    postgreSql_selectQuery="SELECT institution FROM hipolabs.universities ;"

    univTable=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

    combinedSeries=[govTable['AgencyName'],univTable['institution']]

    fullWordbank=pd.concat(combinedSeries)

    wordbankTable=pd.DataFrame(fullWordbank)

    return wordbankTable

def workplaceCompletionTable(inputTable):

    import ossPyFuncs
    import pandas as pd
    import numpy as np



    gitWorkplaceCounts=inputTable['company'].value_counts()
    gitWorplaceAll=gitWorkplaceCounts.index

    workplaceOntology=ossPyFuncs.composeWorkplaceOntology()

    workplacePresentBool=np.in1d(gitWorplaceAll,workplaceOntology)
    
    outTable=gitWorkplaceCounts.reset_index()
    outTable['present']=workplacePresentBool
    outTable.rename(columns={"index":"company name","company":"count"},inplace=True)
    
    return outTable