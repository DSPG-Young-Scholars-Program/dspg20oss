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

unverifiedCompanies.to_csv('/home/dnb3k/git/dspg20oss/ossPy/PackageOuts/diffLibGuesses.csv')

sensibleGuesses=unverifiedCompanies.loc[[6614,6628,6650,6677,6680,6774,6788,6867]]

sensibleGuesses.head(8)


import numpy as np

string1='theironyard'
string2='the iron yard'

string1NoSpaces=string1.replace(' ', '')
string2NoSpaces=string2.replace(' ', '')
onlySpaceDiff=string1NoSpaces==string2NoSpaces

unverifiedCompanies['spaceDiffMap']=''
entriesWithGuesses=unverifiedCompanies.index[unverifiedCompanies['guesses'].str.len()>0]

for iAttempts in range(len(entriesWithGuesses)):
        currentEntry=entriesWithGuesses[iAttempts]
    
        string1=unverifiedCompanies['company'].loc[currentEntry]
        
        currentGuesses=unverifiedCompanies['guesses'].loc[currentEntry]
        
        for iGuesses in range(len(currentGuesses)):
            string2=currentGuesses[iGuesses]
            
            string1NoSpaces=string1.replace(' ', '')
            string2NoSpaces=string2.replace(' ', '')
            string2HasSpaces=string2.find(' ')!=-1
            onlySpaceDiff=string1NoSpaces==string2NoSpaces
            
            if string2HasSpaces & onlySpaceDiff:
                unverifiedCompanies['spaceDiffMap'].loc[currentEntry]=string2
                
                
viewThis=unverifiedCompanies[unverifiedCompanies['spaceDiffMap'].str.len()>0]
            
    
        #place the guesses for each unverified company, if applicable.
        unverifiedCompanies['guesses'].iloc[iAttempts]=difflib.get_close_matches(unverifiedCompanies['company'].iloc[iAttempts],verifiedCompanies['company'],cutoff=0.8)