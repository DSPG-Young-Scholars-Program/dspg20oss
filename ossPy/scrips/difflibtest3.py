#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:24:06 2020

@author: dnb3k
"""

#load precleaned data
cleanedUsers=pd.read_csv('/home/dnb3k/Documents/rawCleanNoNA.csv')

import difflib

tableUniqueFullNameCounts=cleanedUsers['company'].value_counts()
#convert that output to a proper table
tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()

#rename the columns
tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)

thresholdEmployees=5

verifiedCompanies=tableUniqueFullNameCounts['company'].loc[tableUniqueFullNameCounts['count']>thresholdEmployees]
verifiedCompanies=pd.DataFrame(verifiedCompanies)

unverifiedCompanies=tableUniqueFullNameCounts['company'].loc[tableUniqueFullNameCounts['count']<=thresholdEmployees]

unverifiedCompanies=pd.DataFrame(unverifiedCompanies)
unverifiedCompanies['guesses']=''




for iAttempts in range(len(unverifiedCompanies)):
    
    unverifiedCompanies['guesses'].iloc[iAttempts]=difflib.get_close_matches(unverifiedCompanies['company'].iloc[iAttempts],verifiedCompanies['company'],cutoff=0.8)

