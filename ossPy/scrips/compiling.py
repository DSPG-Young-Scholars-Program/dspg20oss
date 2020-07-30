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
withHouseholdColumn=ossPyFuncs.addBooleanColumnFromCriteria(joinedAndReset,houseHoldList,'household')

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

fixedList, fixedReport=ossPyFuncs.spaceSymbolRemap(domiansOutput)

sortedInputColumn, sortedTableUniqueFullNameCounts=ossPyFuncs.uniquePandasIndexMapping(inputColumn)

