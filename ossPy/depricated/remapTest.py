#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:21:06 2020

@author: dnb3k
"""
import pandas as pd
import ossPyFuncs

remapTable=pd.read_csv('workplaceMapping.csv')

postgreSql_selectQuery="SELECT company FROM gh.ctrs_raw ;"

inputColumn=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)


def remapColumnValuesfromTable(inputColumn,remapTable):

    import ossPyFuncs
    import pandas as pd
    import numpy as np
    import difflib



    gitWorkplaceCounts=inputColumn['company'].value_counts()
    sortedTable=gitWorkplaceCounts.reset_index()
    sortedTable.rename(columns={"index":"company name","company":"count"},inplace=True)
   


    workplaceOntology=ossPyFuncs.composeWorkplaceOntology()

    workplacePresentBool=np.in1d(gitWorplaceAll,workplaceOntology)
    
    outTable=gitWorkplaceCounts.reset_index()
    outTable['present']=workplacePresentBool
    outTable.rename(columns={"index":"company name","company":"count"},inplace=True)
    
    return outTable