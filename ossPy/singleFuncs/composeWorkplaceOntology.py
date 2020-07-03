#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 17:56:21 2020

@author: dnb3k
"""


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
