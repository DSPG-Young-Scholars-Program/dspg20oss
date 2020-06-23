#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 21:09:50 2020

@author: dnb3kx`x`
"""
workplaceMapping=pd.read_csv('workplaceMapping.csv',header=None)
worplaceMappingArray=workplaceMapping.to_numpy()

def queryToPDTable(postgreSql_selectQuery):
    import os
    import psycopg2
    import pandas as pd
    import numpy as np

    conn=psycopg2.connect(host="postgis1",
                      dbname="sdad",
                      user=os.environ.get('UVA_uname'),
                      password=os.environ.get('UVA_pass'))

    dataOut=pd.read_sql_query(postgreSql_selectQuery,conn)

    return dataOut


postgreSql_selectQuery="SELECT login, company FROM gh.ctrs_raw ;"

result=queryToPDTable(postgreSql_selectQuery)

result['company'].value_counts()