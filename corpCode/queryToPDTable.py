# -*- coding: utf-8 -*-
"""
Super basic function that returns the output of a mysql query as a pandas table
"""


def queryToPDTable(postgreSql_selectQuery):
    import os
    import psycopg2
    import pandas as pd

    conn=psycopg2.connect(host="postgis1",
                      dbname="sdad",
                      user=os.environ.get('UVA_uname'),
                      password=os.environ.get('UVA_pass'))

    dataOut=pd.read_sql_query(postgreSql_selectQuery,conn)

    return dataOut