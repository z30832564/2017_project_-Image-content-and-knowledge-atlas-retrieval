import pandas as pd
s='刘欣慈写作的一部主人公叫汪淼的书'
rdf_data = pd.read_table('data.txt',sep='\s+')
print(rdf_data)

