#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:39:33 2020

@author: dnb3k
"""
from scipy import sparse
import sys
tableUniqueFullNameCounts=pd.read_csv('/home/dnb3k/Documents/PackageOuts/inOutDegree.csv')
topThousand=tempStore[['company','count']].iloc[0:1000]
tableUniqueFullNameCounts.to_csv('/home/dnb3k/Documents/PackageOuts/inOutDegree.csv')

sparseMatrixHold=sparse.load_npz('/home/dnb3k/Documents/PackageOuts/matrix.npz')

oneRow=accessibleMatrix.todense()

testHold=np.where(oneRow[0,:])
oneRow.todense()

accessibleMatrix=accessibleMatrix.tolil()

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

    

tableUniqueFullNameCounts['countIndegreeOffset']=(tableUniqueFullNameCounts['count']-tableUniqueFullNameCounts['indegree'])>0