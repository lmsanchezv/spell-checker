import pandas as pd
import json, re

matrixs = ['Matriz inserción','Matriz Borrado','Matriz substitución','Matriz intercambio']
filesNames = ['matrixInsert.data','matrixDelete.data','matrixSubs.data','matrixExchange.data']
allData = []
for mat in matrixs:
    data = {}
    df = pd.read_excel('matrices/matrices.xlsx', sheet_name=mat)
    matrix  = df.as_matrix()
    for row in matrix[1:]:
        for index in range(len(row)):
            if len(row) > index + 1: 
                try:
                    value = int(row[index + 1])
                    if value > 0:
                        letter = str(matrix[0,index + 1])
                        key = '%s%s' % (letter,row[0])
                        data[key] = value
                except Exception as inst:
                    print (type(inst))     # the exception instance
                    print (inst.args)    # arguments stored in .args
                    print (inst)           # __str__ allows args to be printed directly
    allData.append(data)

for fil in range(len(filesNames)):
    json_data = json.dumps(allData[fil], ensure_ascii=False)
    with open('matrices/%s' % filesNames[fil], 'w') as f:
        f.write(json_data)