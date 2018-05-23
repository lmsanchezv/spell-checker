from __future__ import division
import ast
import handleAccentuation as ha
import math as calc

class SpellCorrect():
    """Corrector Ortografico usando Language Models, Noisy Channel Model, Error Confusion Matrix and Damerau-Levenshtein Edit Distance."""
    def __init__(self):
        """Método constructor para cargar palabras, matriz de confusión y diccionario."""
        self.nombreDiccionario = "diccionarioCompletoEspanolCR.txt"
        print ('Cargando Diccionario...')
        self.words = sorted(set(self.cargarDiccionario(self.nombreDiccionario)))
        print ('Cargando Biagramas...')
        self.bigrams = self.cargarBigramas('bigramas smoothed.txt')
        print ('Cargando Matriz de Confusion...')
        self.loadConfusionMatrix()
        print ('Carga Completada!!!')
        return
    
    def cargarDiccionario(self, file):
        diccionario = []
        file = open(file)
        for line in file.readlines():
            for v in ha.options:
                    index = line.find(v)
                    if index != -1:
                        newVocal = ha.options[v]()
                        line = line.replace(v, newVocal)
            line = line.strip().lower()
            diccionario.append(line)
        return diccionario
    
    def cargarBigramas(self, file):
        bigrams = {}
        file = open(file)
        for line in file.readlines()[0:1000]:
            line = line.strip().lower()
            line = line.split(',')
            key = '%s %s' % (line[0], line[1])
            bigrams[key] = line[2]
        return bigrams
    
    def dlEditDistance(self, s1, s2):
        """Método para calcular la distancia de edición Damerau-Levenshtein para dos cadenas."""
        s1 = '#' + s1
        s2 = '#' + s2
        m = len(s1)
        n = len(s2)
        D = [[0]*n for i in range(m)]
        for i in range(m):
             for j in range(n):
                 D[i][0] = i
                 D[0][j] = j
        for i in range(m):
            for j in range(n):
                dis=[0]*4
                if i == 0 or j == 0:
                    continue
                dis[0] = D[i-1][j] + 1
                dis[1] = D[i][j-1] + 1
                if s1[i] != s2[j]:
                    dis[2] = D[i-1][j-1] +2
                else:
                    dis[2] = D[i-1][j-1]
                if s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                    dis[3] = D[i-1][j-1] - 1
                if dis[3] != 0:
                    D[i][j] = min(dis[0:4])
                else:
                    D[i][j] = min(dis[0:3])
        return D[m-1][n-1]

    def genCandidates(self, word):
        """Método para generar un conjunto de palabras candidatas para una palabra dada usando Damerau-Levenshtein Edit Distance."""
        candidates = dict()
        print ('Generando palabras candidatas para: %s' % (word))
        for item in self.words:
            #print item, ", ",
            distance = self.dlEditDistance(word, item)
            if distance <= 1:
                candidates[item]=distance
        print ('Palabras Candidatas terminado')
        return sorted(candidates, key=candidates.get, reverse=False)

    def editType(self, candidate, word):
        "Método para calcular el tipo de edición para errores de edición única."
        edit=[False]*4
        correct=""
        error=""
        x=''
        w=''
        for i in range(min([len(word),len(candidate)])-1):
            if candidate[0:i+1] != word[0:i+1]:
                if candidate[i:] == word[i-1:]:
                    edit[1]=True
                    correct = candidate[i-1]
                    error = ''
                    x = candidate[i-2]
                    w = candidate[i-2]+candidate[i-1]
                    break
                elif candidate[i:] == word[i+1:]:
                    
                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#'+error
                    else:
                        w=word[i-1]
                        x=word[i-1]+error
                    edit[0]=True
                    break
                if candidate[i+1:] == word[i+1:]:
                    edit[2]=True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i+1] and candidate[i+2:]==word[i+2:]:
                    edit[3]=True
                    correct = candidate[i]+candidate[i+1]
                    error = word[i]+word[i+1]
                    x=error
                    w=correct
                    break
        candidate=candidate[::-1]
        word=word[::-1]
        for i in range(min([len(word),len(candidate)])-1):
            if candidate[0:i+1] != word[0:i+1]:
                if candidate[i:] == word[i-1:]:
                    edit[1]=True
                    correct = candidate[i-1]
                    error = ''
                    x = candidate[i-2]
                    w = candidate[i-2]+candidate[i-1]
                    break
                elif candidate[i:] == word[i+1:]:
                    
                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#'+error
                    else:
                        w=word[i-1]
                        x=word[i-1]+error
                    edit[0]=True
                    break
                if candidate[i+1:] == word[i+1:]:
                    edit[2]=True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i+1] and candidate[i+2:]==word[i+2:]:
                    edit[3]=True
                    correct = candidate[i]+candidate[i+1]
                    error = word[i]+word[i+1]
                    x=error
                    w=correct
                    break
        if word == candidate:
            return "None", '', '', '', ''
        if edit[1]:
            return "Deletion", correct, error, x, w
        elif edit[0]:
            return "Insertion", correct, error, x, w
        elif edit[2]:
            return "Substitution", correct, error, x, w
        elif edit[3]:
            return "Reversal", correct, error, x, w
        

    def loadConfusionMatrix(self):
        """Método para cargar la Matrix de Confusion desde un archivo de datos externo."""
        f=open('matrices/matrixInsert.data', 'r')
        data=f.read()
        f.close
        self.addmatrix=ast.literal_eval(data)
        f=open('matrices/matrixSubs.data', 'r')
        data=f.read()
        f.close
        self.submatrix=ast.literal_eval(data)
        f=open('matrices/matrixExchange.data', 'r')
        data=f.read()
        f.close
        self.revmatrix=ast.literal_eval(data)
        f=open('matrices/matrixDelete.data', 'r')
        data=f.read()
        f.close
        self.delmatrix=ast.literal_eval(data)

    def channelModel(self, x,y, edit):
        """Método para calcular la probabilidad del channel model para errores."""
        corpus = ' '.join(self.words)
        if edit == 'add':
            if x == '#':
                return self.addmatrix[x+y]/corpus.count(' '+y)
            else:
                return self.addmatrix[x+y]/corpus.count(x)
        if edit == 'sub':
            return self.submatrix[(x+y)[0:2]]/corpus.count(y)
        if edit == 'rev':
            return self.revmatrix[x+y]/corpus.count(x+y)
        if edit == 'del':
            return self.delmatrix[x+y]/corpus.count(x+y)
#help(SpellCorrect)
sc = SpellCorrect()

while True:
    sentence = str(input('Entre oracion a corregir: ').lower()).split() #"sto s ola mundo".lower().split()
    correct=""    
    for index, word in enumerate(sentence):
        candidates = sc.genCandidates(word)
        if word in candidates:
            correct=correct+word+' '
            continue
        #print word, ': ', candidates
        NP=dict()
        P=dict()
        for item in candidates:
            try:
                edit = sc.editType(item, word)
                #print item, ': ' , edit
                if edit == None: continue
                if edit[0] == "Insertion":
                    NP[item] = sc.channelModel(edit[3][0],edit[3][1], 'add')
                if edit[0] == 'Deletion':
                    NP[item] = sc.channelModel(edit[4][0], edit[4][1], 'del')
                if edit[0] == 'Reversal':
                    NP[item] = sc.channelModel(edit[4][0], edit[4][1], 'rev')
                if edit[0] == 'Substitution':
                    NP[item] = sc.channelModel(edit[3], edit[4], 'sub')
            except Exception as inst:
                print (type(inst))     # the exception instance
                print (inst.args)     # arguments stored in .args
                print (inst)           # __str__ allows args to be printed directly
        for item in NP:
            channel = NP[item]
            if len(sentence)-1 != index:
                print ('todo')
                key = sentence[index-1]+ ' ' + item#+sentence[index+1]
                probability = sc.bigrams.get(key,0)
                probability = calc.pow(calc.e, probability)
                bigram = calc.pow(calc.e, probability)
            else:
                print ('todo')
                key = sentence[index-1]+ ' ' + item
                probability = sc.bigrams.get(key,0)
                probability = calc.pow(calc.e, probability)
                bigram = calc.pow(probability)
            P[item] = channel*bigram*calc.pow(10,9)
        P = sorted(P, key=P.get, reverse=True)
        if P == []:
            P.append('')
        correct = correct +P[0] +' '
        
    print ('Response: '+correct)
