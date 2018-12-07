# -*- coding:utf-8 -*-
import rdflib
import pymongo
import string
from rdflib.namespace import RDF, FOAF
import pandas as pd
s = 'http://www.example.org/'
l = '<'
r = '>'
class Queryer:
    def __init__(self,list):
        self.l = list
    def Query(self):
        '''q = 'select ?x where { ?x'+l+s+self.a+r + ' '+l+s+self.b+r+'}'
        g = rdflib.Graph()
        g.parse("app/kg/graph.rdf", format="n3")
        x = g.query(q)
        x = list(x)
        for i in range(len(x)):
            print(x[i][0])
            a = x[i][0].split('org/')[1]
        '''

        db = pymongo.MongoClient()
        features = db.features
        index = features.tindex
        tindex = index.find()
        L = []
        L.extend(tindex)
        result = []
        for i in self.l:
            for book in L:
                if book['书名'] == i:
                    result.append((book['书名'], book['书号']))
                if book['书号'] == i:
                    result.append((book['书名'], book['书号']))
                if book['作者'] == i:
                    result.append((book['书名'], book['书号']))
                if book['译者'] == i:
                    result.append((book['书名'], book['书号']))
                if book['出版社'] == i:
                    result.append((book['书名'], book['书号']))
                if book['版次'] == i:
                    result.append((book['书名'], book['书号']))
                if book['定价'] == i:
                    result.append((book['书名'], book['书号']))
                if book['馆藏地'] == i:
                    result.append((book['书名'], book['书号']))
                if book['数量'] == i:
                    result.append((book['书名'], book['书号']))
        result = list(set(result))
        print(result)
        if len(result)>0:
            return result
        else:
            return [('没有找到',1111111111)]



