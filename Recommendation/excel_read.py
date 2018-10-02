# -*- coding: utf-8 -*-


import pandas as pd
import pymysql

db = pymysql.connect("localhost", "root", "123456", "testdb", charset="utf8")
df = pd.read_sql('select * from category;', con=db)   
print(df.head()) 
db.close()
