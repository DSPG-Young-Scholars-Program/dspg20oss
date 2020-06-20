#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:03:22 2020

@author: dnb3k
"""

def expandAbreviations(inputColumn,expansionList):
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
        curReplaceVal=row[0]
        currentRegexExpression=curReplaceVal + '(?i)'
    
        inputColumn.replace(regex=currentRegexExpression, value='', inplace=True)


   return inputColumn

