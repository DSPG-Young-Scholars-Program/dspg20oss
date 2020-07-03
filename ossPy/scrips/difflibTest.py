#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 19:47:13 2020

@author: dnb3k
"""

lesserCompanies=multiCoWorkerTable.iloc[15000:-1]
lesserCompanies['guesses']=""

import difflib

df['Name_r'] = df.Name_x.map(lambda x: (difflib.get_close_matches(x, dfF.Name)[:1] or [None])[0]) 

df2.index = df2.index.map(lambda x: difflib.get_close_matches(x, multiCoWorkerTable.index)[0])

for iAttempts in range(len(lesserCompanies.index)):
    
    currentNameRange=range(0,1000+iAttempts)
    lesserCompanies['guesses'].iloc[iAttempts]=difflib.get_close_matches(lesserCompanies['company'].iloc[iAttempts],multiCoWorkerTable['company'].iloc[currentNameRange],cutoff=0.8)

lesserCompanies['guesses'].iloc[iAttempts]