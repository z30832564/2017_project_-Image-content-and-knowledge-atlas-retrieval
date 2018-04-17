import pymongo
import pandas as pd
data = pd.read_table('data1.txt', sep='\s+')
columns = list(data.columns)
# mongodb数据库初始化
db = pymongo.MongoClient()
book_data = db.book_data
index = book_data.tindex
for i in range(len(data)):
    f = {}
    for j in range(len(columns)):
        print(j)
        f[columns[j]] = str(data.loc[i][j])
    f[]
    index.insert_one(f)
