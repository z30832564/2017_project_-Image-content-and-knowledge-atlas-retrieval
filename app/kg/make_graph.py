# -*- coding: utf-8 -*-
import pandas as pd
import rdflib
data = pd.read_table("data.txt", sep='\s+')
s='http://www.example.org/'
g = rdflib.Graph()

for i in range(len(data)):
    a = rdflib.URIRef(s+''.join(data.loc[i][0]))
    b = rdflib.URIRef(s+''.join(data.loc[i][1]))
    c = rdflib.URIRef(s+''.join(data.loc[i][2]))
    g.add((a,b,c))

g.serialize("graph.rdf", format='n3')
g1 = rdflib.Graph()
g1.parse("graph.rdf", format="n3")

print(list(g1))