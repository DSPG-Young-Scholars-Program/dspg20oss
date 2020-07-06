#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:57:39 2020

@author: dnb3k
"""

cleanedData=pd.read_csv('/home/dnb3k/Documents/newCleaned.csv')
cleanedData.dropna( inplace=True)
cleanedData=cleanedData.drop(columns=['Unnamed: 0'])




#apply replacements
currentDir=os.path.dirname('ossPyFuncs.py')
replaceList=pd.read_csv(os.path.join(currentDir,'keyFiles/expandAbrevs.csv'),quotechar="'",header=None)
replacedOutput, replaceList=ossPyFuncs.expandFromColumn(inputLower['company'],replaceList)
replacedOutput=pd.DataFrame(replacedOutput)

print(str(np.sum(replaceList['changeNum'])) + ' listings changed by replacemnt method')

#remove legal entity abreviations
LElist=pd.read_csv(os.path.join(currentDir,'keyFiles/curatedLegalEntitesRaw.csv'),quotechar="'",header=None)
LEoutput, LEeraseList=ossPyFuncs.eraseFromColumn(replacedOutput['company'],LElist)
LEoutput=pd.DataFrame(LEoutput)

print(str(np.sum(LEeraseList['changeNum'])) + ' listings changed by legal entity removal method')

#remove domain names
domainList=pd.read_csv(os.path.join(currentDir,'keyFiles/curatedDomains.csv'),quotechar="'",header=None)
domainOutput, DomainEraseList=ossPyFuncs.eraseFromColumn(LEoutput['company'],domainList)
domainOutput=pd.DataFrame(domainOutput)

print(str(np.sum(DomainEraseList['changeNum'])) + ' listings changed by web domain method')

#remove symbols
symbolList=pd.read_csv(os.path.join(currentDir,'keyFiles/symbolRemove.csv'),quotechar="'",header=None)
symbolOut, symbolEraseList=ossPyFuncs.eraseFromColumn(domainOutput['company'],symbolList)
symbolOut=pd.DataFrame(symbolOut)

print(str(np.sum(symbolEraseList['changeNum'])) + ' listings changed by symbol method')

symbolOut=pd.DataFrame(symbolOut['company'].str.lower())


#now for unique full names
tableUniqueFullNameCounts=symbolOut.iloc[:,0].value_counts()
#convert that output to a proper table
tableUniqueFullNameCounts=tableUniqueFullNameCounts.reset_index()

#rename the columns
tableUniqueFullNameCounts.rename(columns={"company":"count","index":"company"},inplace=True)
tableUniqueFullNameCounts=tableUniqueFullNameCounts[~tableUniqueFullNameCounts['company'].str.contains("^$")]

#create some new columns
tableUniqueFullNameCounts['guesses']=''
tableUniqueFullNameCounts['guessesIndexes']=''
tableUniqueFullNameCounts['additionalIndividuals']=0
tableUniqueFullNameCounts['timesCounted']=0


tableUniqueFullNameCounts=tableUniqueFullNameCounts[~tableUniqueFullNameCounts['company'].isna()]



#iterate acroos unique listings
for index, row in tableUniqueFullNameCounts.iterrows():
    
    #formulate a good regex expression
    currentRegex=re.compile('(?i)\\b'+re.escape(tableUniqueFullNameCounts['company'].loc[index])+'\\b')
    
    #get all company listings that feature the current company string
    currentBool=tableUniqueFullNameCounts['company'].str.contains(currentRegex)
    #get the indexes associated with those names
    currentIndexes=currentBool[currentBool].index
    tableUniqueFullNameCounts['guessesIndexes'].loc[index]=currentIndexes
    tableUniqueFullNameCounts['timesCounted'].loc[currentIndexes]=tableUniqueFullNameCounts['timesCounted'].loc[currentIndexes].add(1)  
     #find the number of additional individuals that are found with
    #the regex search
    currentAdditionalIndividuals=np.sum(tableUniqueFullNameCounts['count'].loc[currentIndexes])-tableUniqueFullNameCounts['count'].loc[index]
    #resort the indexes such that the first listing has the
    #most number of employees associated with it
    currentGeusses= tableUniqueFullNameCounts['company'].loc[currentIndexes.sort_values()]
    #create a full string vector of these company names, and place it in the new column
    tableUniqueFullNameCounts['guesses'].loc[index]= currentGeusses.str.cat(sep=' /// ')
    #place the additional sum in its new column
    tableUniqueFullNameCounts['additionalIndividuals'].loc[index]= currentAdditionalIndividuals
    
tableUniqueFullNameCounts.to_csv('/home/dnb3k/Documents/CompleteRemap.csv')
testHold=tableUniqueFullNameCounts['guessesIndexes'].to_numpy()

testHold[1]

np.isin(0,testHold)

dataTest3=tableUniqueFullNameCounts[tableUniqueFullNameCounts['guessesIndexes'].apply(==0)]