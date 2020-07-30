#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:24:06 2020

@author: dnb3k
"""

Ontology=ossPyFuncs.composeWorkplaceOntology()

lesserCompanies=multiCoWorkerTable.iloc[15000:-1]
lesserCompanies['guesses']=""
multiCoWorkerTable['guesses']=""

import difflib

#df['Name_r'] = df.Name_x.map(lambda x: (difflib.get_close_matches(x, dfF.Name)[:1] or [None])[0]) 

#df2.index = df2.index.map(lambda x: difflib.get_close_matches(x, multiCoWorkerTable.index)[0])

for iAttempts in range(len(multiCoWorkerTable.index)):
    
    multiCoWorkerTable['guesses'].iloc[iAttempts]=difflib.get_close_matches(multiCoWorkerTable['company'].iloc[iAttempts],Ontology[0],cutoff=0.8)

lesserCompanies['guesses'].iloc[iAttempts]