from __future__ import division
from collections import Counter
import math as calc

class BigramasUnigramas():
    def __init__(self, uni=False, bi=False):
        """Método de constructor que carga el corpus desde el archivo y crea ngrams basados en los parámetros de entrada."""
        self.words=self.cargarCorpus()
        if uni : self.unigram=self.crearUnigrama(self.words)
        if bi : self.bigram=self.crearBigrama(self.words)
        return

    def cargarCorpus(self):
        """Método para cargar un archivo externo que contiene el corpus sin procesar"""
        print ("Cargando el Corpus solicitado")
        corpusfile = open('corpus.data', 'r' , encoding="utf8")
        corpus = corpusfile.read()
        corpusfile.close()
        print ("Procesando el Corpus")
        words = corpus.split(' ')
        return words
    
    def crearUnigrama(self, words):
        """Método para crear un modelo de Unigramas para las palabras cargadas desde el corpus."""
        print("Creating Unigram Model")
        unigram = dict()
        #unigramfile = open('unigram.data', 'w')
        print("Cálculo del conteo para el modelo de Unigramas")
        unigram = Counter(words)
        #unigramfile.write(str(unigram))
        #unigramfile.close()
        return unigram

    def crearBigrama(self, words):
        """Method to create Bigram Model for words loaded from corpus."""
        print("CrCreando el modelo de Biagramas")
        biwords = []
        for index, item in enumerate(words):
            if index==len(words)-1:
                break
            biwords.append(item+' '+words[index+1])
        print("Calculando el numero de Biagramas para el modelo")
        bigram = dict()
        #bigramfile = open('bigram.data', 'w')
        bigram = Counter(biwords)
        #bigramfile.write(str(bigram))
        #bigramfile.close()
        return bigram

    def probabilidad(self, word, words = "", gram = 'uni'):
        """Método para calcular la  máxima Likelihood Probability de n-Grams basado en varios parámetros."""
        if gram == 'uni':
            return calc.log((self.unigram[word]+1)/(len(self.words)+len(self.unigram)))
        elif gram == 'bi':
            return calc.log((self.bigram[words]+1)/(self.unigram[word]+len(self.unigram)))

    def probabilidadOracion(self, sent, gram='uni', form='antilog'):
        """Método para calcular el n-gram acumulativo Probabilidad y el máximo  Likelihood Probability de una frase u oración."""
        words = sent.lower().split()
        P=0
        if gram == 'uni':
            for index, item in enumerate(words):
                P = P + self.probabilidad(item)
        if gram == 'bi':
            for index, item in enumerate(words):
                if index == len(words)- 1: break
                P = P + self.probabilidad(item, item+' '+words[index+1], 'bi')
        if form == 'log':
            return P
        elif form == 'antilog':
            return calc.pow(calc.e, P)

#help(nGram)
# ng = nGram(True, True, False, False, False)
# print (ng.sentenceprobability('hold your horses', 'bi', 'log'))