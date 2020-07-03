#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 16:18:55 2020

@author: dnb3k
"""
def workplaceGuessTable(inputTable):

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