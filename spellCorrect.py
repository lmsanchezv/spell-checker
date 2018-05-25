from __future__ import division
import ast, json, os, collections
import handleAccentuation as ha
import math as calc
from multiprocessing import Process
import multiprocessing as mp
from multiprocessing import Manager
import pyxdameraulevenshtein as px
from BigramasUnigramas import BigramasUnigramas


d = collections.defaultdict(list)
class SpellCorrect():
    """Corrector Ortografico usando Language Models, Noisy Channel Model, Error Confusion Matrix and Damerau-Levenshtein Edit Distance."""
    def __init__(self):
        """Método constructor para cargar palabras, matriz de confusión y diccionario."""
        print ('Cargando Diccionario...')
        self.words = []
        self.bigrams = {}
        self.cargarDiccionario('diccionarioCompletoEspanolCR.txt')
        self.words = sorted(set(self.words))
        self.bigrams = BigramasUnigramas(True, True)
       # self.cargarBigramas('bigramas smoothed.txt')
        print ('Cargando Matriz de Confusion...')
        self.loadConfusionMatrix()
        print ('Carga Completada!!!')
        return
    
    def cargarDiccionario2(self, file):
        diccionario = []
        file = open(file, encoding="utf8")
        for line in file.readlines():
            for v in ha.options:
                    index = line.find(v)
                    if index != -1:
                        newVocal = ha.options[v]()
                        line = line.replace(v, newVocal)
            line = line.strip().lower()
            diccionario.append(line)
        return diccionario
    
    def cargarBigramas2(self, file):
        bigrams = {}
        file = open(file)
        for line in file.readlines()[0:1000]:
            line = line.strip().lower()
            line = line.split(',')
            key = '%s %s' % (line[0], line[1])
            bigrams[key] = line[2]
        return bigrams

    def split(self, l):
        return l.split()

    def cargarBigramas(self, archivoOrigen):
        cores = mp.cpu_count()
        pool = mp.Pool(processes=cores)
        f = open(archivoOrigen, 'r', encoding="utf8")
        for keys in pool.map(self.split, f.readlines()[0:1000]):
            line = keys[0].strip().lower()
            line = line.split(',')
            key = '%s %s' % (line[0], line[1])
            self.bigrams[key] = line[2]
        pool.close()

    def cargarDiccionario(self, archivoOrigen):
        cores = mp.cpu_count()
        pool = mp.Pool(processes=cores)
        for keys in pool.map(self.split, open(archivoOrigen, encoding="utf8")):
            self.words.append(keys[0])
        pool.close()

    def dlEditDistance(self, s1, s2):
        """Método para calcular la distancia de edición Damerau-Levenshtein para dos cadenas."""
        d = {}
        lenstr1 = len(s1)
        lenstr2 = len(s2)
        for i in range(-1,lenstr1+1):
            d[(i,-1)] = i+1
        for j in range(-1,lenstr2+1):
            d[(-1,j)] = j+1
    
        for i in range(lenstr1):
            for j in range(lenstr2):
                if s1[i] == s2[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i,j)] = min(
                            d[(i-1,j)] + 1, # deletion
                            d[(i,j-1)] + 1, # insertion
                            d[(i-1,j-1)] + cost, # substitution
                            )
                if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                    d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition
 
        return d[lenstr1-1,lenstr2-1]

    def genCandidates2(self, word):
        """Método para generar un conjunto de palabras candidatas para una palabra dada usando Damerau-Levenshtein Edit Distance."""
        cores = mp.cpu_count()
        pool = mp.Pool(processes=cores)
        candidates = dict()
        for keys in pool.map(self.split, self.words):
            distance = self.dlEditDistance(word, keys[0])
            if distance <= 1:
                candidates[keys[0]]=distance
        pool.close()
        return sorted(candidates, key=candidates.get, reverse=False)

    def genCandidates(self, word, words, return_dict):
        """Método para generar un conjunto de palabras candidatas para una palabra dada usando Damerau-Levenshtein Edit Distance."""
        #candidates = dict()
        for item in words:
            #print item, ", ",
            distance = px.damerau_levenshtein_distance(word, item)#self.dlEditDistance(word, item)
            if distance <= 1:
                return_dict.append(item)
    
    def split_work(self, word):
        manager = mp.Manager()
        return_dict = manager.list()
        #print ('Generando palabras candidatas para: %s' % (word))
        lenght = int(len(self.words) / 4)
        start = 0
        end = 0
        processes = []
        if word not in self.words:
            for i in range(4):
                start = end
                end = (i + 1) * lenght
                p = Process(target=self.genCandidates, args=(word, self.words[start:end], return_dict))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
        else:
            return_dict.append(word)
        return sorted(return_dict, key=str.lower, reverse=False)

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
        data=json.load(f)
        f.close
        self.addmatrix=ast.literal_eval(data)
        f=open('matrices/matrixSubs.data', 'r')
        data=json.load(f)
        f.close
        self.submatrix=ast.literal_eval(data)
        f=open('matrices/matrixExchange.data', 'r')
        data=json.load(f)
        f.close
        self.revmatrix=ast.literal_eval(data)
        f=open('matrices/matrixDelete.data', 'r')
        data=json.load(f)
        f.close
        self.delmatrix=ast.literal_eval(data)

    def channelModel(self, x,y, edit):
        """Método para calcular la probabilidad del channel model para errores."""
        try:
            corpus = ' '.join(self.bigrams.words)
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
        except Exception as inst:
            #print ('Combinacion ' +inst.args[0] + ' no encontrada en la matriz de ' + edit)
            return 0
#help(SpellCorrect)

def crearCorrector():
    sc = SpellCorrect()

    while True:
        sentence = str(input('Entre oracion a corregir: ').lower()).split() 
        if len(sentence) == 1 and sentence[0] == 'salir':
            print ('Proceseso terminado')
            break
        correct=""    
        for index, word in enumerate(sentence):
            candidates = sc.split_work(word)
            if word in candidates:
                correct=correct+word+' '
                continue
            #print word, ': ', candidates
            NP=dict()
            P=dict()
            for item in candidates:
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
            for item in NP:
                channel = NP[item]
                if len(sentence)-1 != index:
                    key = sentence[index-1]+ ' ' + item + ' ' +sentence[index+1]
                    #probability = sc.bigrams.get(key,0)
                    #probability = calc.pow(calc.e, probability)
                    #bigram = calc.pow(calc.e, probability)
                    bigram = calc.pow(calc.e, sc.bigrams.probabilidadOracion(key, 'bi', 'antilog'))
                else:
                    #key = '<s> ' + item
                    #probability = sc.bigrams.get(key,0)
                    #probability = calc.pow(calc.e, probability)
                    #bigram = calc.pow(calc.e, probability)
                    bigram = calc.pow(calc.e, sc.bigrams.probabilidadOracion(sentence[index-1]+ ' ' + item, 'bi', 'antilog'))
                P[item] = channel*bigram*calc.pow(10,9)
            P = sorted(P, key=P.get, reverse=True)
            if P == []:
                P.append('')
            correct = correct +P[0] +' '
            
        print ('Oracion Corregida: '+correct)

if __name__ == '__main__':  
    crearCorrector()