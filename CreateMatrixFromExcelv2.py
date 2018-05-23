import pandas as pd
import json, re
from collections import defaultdict

filesNames = ['matrixInsert.data','matrixDelete.data','matrixSubs.data','matrixExchange.data']
allData = [defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list)]
data = []
df = pd.read_excel('matrices/matrices.xls')
matrix  = df.as_matrix()
for row in matrix[1:]:
    i = -1
    if row[2] == "Substitucion":
        i = 2
    elif row[2] == "Borrado":
        i = 1
    elif row[2] == "Insercion":
        i = 0
    elif row[2] == "Intercambio":
        i = 3

    if i >= 0:
        if row[3]+row[4] in allData[i]:
            allData[i][row[3]+row[4]] += 1
        else:
            allData[i][row[3]+row[4]] = 1
        print (allData[i][row[3]+row[4]])

for fil in range(len(filesNames)):
    json_data = json.dumps(allData[fil], ensure_ascii=False)
    with open('matrices/%s' % filesNames[fil], 'w') as outfile:
        json.dump(json_data, outfile)