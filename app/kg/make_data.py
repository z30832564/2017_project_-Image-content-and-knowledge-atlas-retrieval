import pymongo
import pandas as pd
data1 = pd.read_table('../data1.txt', sep='\s+').astype('str')
columns = list(data1.columns)
data = open('data.txt','w',encoding='utf-8')
for i in range(len(data1)):
    print(data1['书名'][i])
    data.write(data1['书名'][i]+' 书号 '+data1['书号'][i]+'\n')
    data.write(data1['书名'][i] + ' 作者 ' + data1['作者'][i] + '\n')
    data.write(data1['书名'][i] + ' 出版社 ' + data1['出版社'][i] + '\n')
    data.write(data1['书名'][i] + ' 封面地址 ' + data1['封面地址'][i] + '\n')
    data.write(data1['书名'][i] + ' 译者 ' + data1['译者'][i] + '\n')
    data.write(data1['书名'][i] + ' 版次 ' + data1['版次'][i] + '\n')
    data.write(data1['书名'][i] + ' 定价 ' + data1['定价'][i] + '\n')
    data.write(data1['书名'][i] + ' 馆藏地 ' + data1['馆藏地'][i] + '\n')
    data.write(data1['书名'][i] + ' 数量 ' + data1['数量'][i] + '\n')
    data.write(data1['书名'][i] + ' 在架数量 ' + data1['在架数量'][i] + '\n')
    data.write(data1['书名'][i] + ' 应还日期 ' + data1['应还日期'][i] + '\n')
    data.write(data1['出版社'][i] + ' 出版 ' + data1['书名'][i] + '\n')
    data.write(data1['作者'][i] + ' 写作 ' + data1['书名'][i] + '\n')
    data.write(data1['馆藏地'][i] + ' 藏书 ' + data1['书名'][i] + '\n')
    if data1['译者'][i] != '无':
        data.write(data1['译者'][i] + ' 翻译 ' + data1['书名'][i] + '\n')
print(data)
