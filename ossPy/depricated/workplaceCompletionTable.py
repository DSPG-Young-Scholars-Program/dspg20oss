#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 16:18:55 2020

@author: dnb3k
"""
def workplaceCompletionTable(inputTable):
    """Return the output of a SDAD mysql query as a table
    
    Keyword arguments:
    inputTable -- a properly formatted mysql query
   
    """
    import ossPyFuncs
    import pandas as pd
    import numpy as np

    
    gitWorkplaceCounts=inputTable['company'].value_counts()
    gitWorplaceAll=gitWorkplaceCounts.index
    #rename the columns
    tableUniqueCounts.rename(columns={"index":"company name","company":"count"},inplace=True)

    workplaceOntology=ossPyFuncs.composeWorkplaceOntology()

    workplacePresentBool=np.in1d(gitWorplaceAll,workplaceOntology)
    
    outTable=gitWorkplaceCounts.reset_index()
    outTable['present']=workplacePresentBool
    outTable.rename(columns={"index":"company name","company":"count"},inplace=True)
    
    return outTable