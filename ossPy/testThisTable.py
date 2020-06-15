#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:46:17 2020

@author: dnb3k
"""

import ossPyFuncs



postgreSql_selectQuery="SELECT login, company FROM gh.ctrs_raw ;"

inputTable=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)


presentCountTable=ossPyFuncs.workplaceCompletionTable(inputTable)