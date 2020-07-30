#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:39:33 2020

@author: dnb3k
"""
from scipy import sparse
import sys

tableUniqueFullNameCounts=pd.read_csv('/home/dnb3k/git/dspg20oss/ossPy/PackageOuts/ratioIndegree.csv')
tableUniqueFullNameCounts=tableUniqueFullNameCounts.rename(columns={"indegree":"outdegree1","outdegree":"indegree","outdegree1":"outdegree"})
tableUniqueFullNameCounts=tableUniqueFullNameCounts.rename(columns={"outdegree1":"outdegree"})

tableUniqueFullNameCounts=tableUniqueFullNameCounts[['company','count','outdegree','indegree']]
tableUniqueFullNameCounts.to_csv('/home/dnb3k/Documents/PackageOuts/inOutDegree.csv')

sparseMatrixHold=sparse.load_npz('/home/dnb3k/Documents/PackageOuts/matrix.npz')

oneRow=accessibleMatrix.todense()

testHold=np.where(oneRow[0,:])
oneRow.todense()

sparseMatrixHold=sparseMatrixHold.tolil()

print(sys.getsizeof(accessibleMatrix))

indexesStore=np.where(accessibleMatrix)

totalEntries=np.sum(tableUniqueFullNameCounts['count'])

tableUniqueFullNameCounts=tableUniqueFullNameCounts[['company','count']]

tableUniqueFullNameCounts['reachability']=''
tableUniqueFullNameCounts['maxReachable']=0



for index, row in tableUniqueFullNameCounts.iterrows():
    
    nodeArray , predecessors=scipy.sparse.csgraph.depth_first_order(sparseMatrixHold,index)
    
    tableUniqueFullNameCounts['reachability'].loc[index]=nodeArray
    tableUniqueFullNameCounts['maxReachable'].loc[index]=np.min(nodeArray)

sparseMatrixHold=sparseMatrixHold.todense()    
np.count_nonzero(sparseMatrixHold[index,:])


tableUniqueFullNameCounts['countIndegreeOffset']=(tableUniqueFullNameCounts['count']-tableUniqueFullNameCounts['indegree'])>0

nonOneDegree=np.where(tableUniqueFullNameCounts['outdegree']>1)[0]



tableUniqueFullNameCounts['defactoRoot']=True

for iIndex in nonOneDegree:
    
    print(iIndex)
    
    currentSubstringIndexes,_,_=sparse.find(sparseMatrixHold[:,iIndex])
    
    currentSubstringIndexes=np.append(currentSubstringIndexes, iIndex)
    
    currentCounts=tableUniqueFullNameCounts['count'].loc[currentSubstringIndexes]
    
    if currentCounts.loc[iIndex]==np.max(currentCounts):
    
        tableUniqueFullNameCounts['defactoRoot'].loc[iIndex]=True
    else:
        tableUniqueFullNameCounts['defactoRoot'].loc[iIndex]=False
    

