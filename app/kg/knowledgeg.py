# -*- coding:utf-8 -*-
import rdflib
import pymongo
import string
from rdflib.namespace import RDF, FOAF
s = 'http://www.example.org/'
l = '<'
r = '>'
class Queryer:
    def __init__(self,l):
        self.l = l
        self.a = l[0]
        self.b = l[1]
    def Query(self):
        q = 'select ?x where { ?x'+l+s+self.a+r + ' '+l+s+self.b+r+'}'
        g = rdflib.Graph()
        g.parse("app/kg/graph.rdf", format="n3")
        x = g.query(q)
        x = list(x)
        for i in range(len(x)):
            a = x[i].split('/')
            x[i] = a[2]
        db = pymongo.MongoClient()
        book_data = db.book_data
        index = book_data.tindex
        tindex = index.find()
        L = []
        L.extend(tindex)
        for book in L:
            if book['书名'] == x[0]:
                return book['书名'], book['封面地址']

