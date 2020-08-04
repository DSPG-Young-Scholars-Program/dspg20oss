#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 18:37:02 2020

@author: dnb3k
"""



postgreSql_selectQuery="SELECT login, company_cleaned, is_academic FROM gh.sna_ctr_academic ;"
academicCleaned=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

postgreSql_selectQuery="SELECT login, is_gov FROM gh.sna_ctr_gov ;"
govData=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

postgreSql_selectQuery="SELECT login, company FROM gh.ctrs_raw ;"
fullData=ossPyFuncs.queryToPDTable(postgreSql_selectQuery)

joinedData1=fullData.set_index('login').join(academicCleaned.set_index('login'))

joinedData2=joinedData1.join(govData.set_index('login'))

joinedAndReset=joinedData2.reset_index()

currentDir=os.path.dirname('ossPyFuncs.py')

houseHoldList=pd.read_csv(os.path.join(currentDir,'keyFiles/individualKeys.csv'),quotechar="'",header=None)
withHouseholdColumn=ossPyFuncs.addBooleanColumnFromCriteria(pd.DataFrame(joinedAndReset['company'],houseHoldList,'household')

noneList=pd.read_csv(os.path.join(currentDir,'keyFiles/nullKeys.csv'),quotechar="'",header=None)
withNoneColumn=ossPyFuncs.addBooleanColumnFromCriteria(withHouseholdColumn,noneList,'null')

naReplaced=withNoneColumn[['is_gov','is_academic']].fillna(value=False)

fixedDataframe=withNoneColumn.assign(is_gov=naReplaced['is_gov'],is_academic=naReplaced['is_academic'])

alreadyAssigned=fixedDataframe[['is_gov','is_academic','household','null']].any(axis=1)

onlyUnassignedFrame=fixedDataframe.loc[~alreadyAssigned]


#begin cleaning


#construct path to legal entity list and erase them
LElist=pd.read_csv(os.path.join(currentDir,'keyFiles/curatedLegalEntitesRaw.csv'),quotechar="'",header=None)
LEoutput, LEeraseList=ossPyFuncs.eraseFromColumn(onlyUnassignedFrame['company'],LElist)

#construct path to legal symbol list and erase them
symbollist=pd.read_csv(os.path.join(currentDir,'keyFiles/symbolRemove.csv'),quotechar="'",header=None)
Symboloutput, symbolEraseList=ossPyFuncs.eraseFromColumn(LEoutput,symbollist)

domainsList=pd.read_csv(os.path.join(currentDir,'keyFiles/curatedDomains.csv'),quotechar="'",header=None)
domiansOutput, domainsEraseList=ossPyFuncs.eraseFromColumn(Symboloutput,domainsList)

#fixedList, fixedReport=ossPyFuncs.spaceSymbolRemap(domiansOutput)
sortedInputColumn, sortedTableUniqueFullNameCounts=ossPyFuncs.uniquePandasIndexMapping(pd.DataFrame(domiansOutput))
    
namesWithMapping=sortedTableUniqueFullNameCounts.set_index('index')
namesWithMapping=namesWithMapping.sort_index()
#+1 because we are using greater than or equal to
#we'll also be using this vector to obtain our user remapping
threshold=5
aboveThresholdBoolVec=namesWithMapping['count'].ge(threshold+1)

totalUsersAboveThreshold=np.sum(namesWithMapping['count'].loc[aboveThresholdBoolVec])
#may need to resort this in order to get it to line up with origional
superThresholdIndexSubframe=namesWithMapping['inputIndexMapping'].loc[aboveThresholdBoolVec]

concatIndexArray=np.empty([1],dtype=int)
for index, value in superThresholdIndexSubframe.iteritems():
    concatIndexArray=np.concatenate([concatIndexArray,superThresholdIndexSubframe.loc[index].to_numpy()])

joinedAndReset['is_business']=False
joinedAndReset['is_business'].loc[concatIndexArray]=True
joinedAndReset['company_cleaned']=domiansOutput


testMerge=joinedAndReset.merge(pd.DataFrame(onlyUnassignedFrame[['company_cleaned]])

joinedData3=joinedAndReset.set_index('login').join(onlyUnassignedFrame.set_index('login'))

joinedAndResetOut=joinedData3.reset_index()



fullData['is_business']=False
#somehow need to flatten, use np.ravel for this 
fullData['is_business'].loc[np.ravel(subjectIndexArray)]=True

