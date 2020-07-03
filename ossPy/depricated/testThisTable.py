#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:46:17 2020

@author: dnb3k
"""

import ossPyFuncs



postgreSql_selectQuery="SELECT c,ompany FROM gh.ctrs_raw ;"
inputRawColumn=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

postgreSql_selectQuery="SELECT login, company FROM gh.ctrs_raw ;"
inputRaw=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)


targetOntology=ossPyFuncs.composeWorkplaceOntology()

assessTable=ossPyFuncs.checkColumnMapping(inputRawColumn,targetOntology)

dataTest=assessTable['company'].str.contains("Microsoft")

presentCountTable=ossPyFuncs.workplaceCompletionTable(inputTable)