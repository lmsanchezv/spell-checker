# -*- coding: 850 -*-
import os
from ElapsedTimeFormatter import ElapsedFormatter
import logging
import codecs,  handleAccentuation as ha

nombreDiccionario = "diccionarioCompletoEspanolCR.txt"
nombreArchivoErrores = ["Errores1.html","Errores2.html","Errores3.html"]
archivoOrigen = "output.txt"
palabrasOmitir = ["<s>","</s>","xxurlxx","xxnumxx"]

diccionario = []

def cargarDiccionario(file):
    file = open(file)
    for line in file.readlines():
        for v in ha.options:
                index = line.find(v)
                if index != -1:
                    newVocal = ha.options[v]()
                    line = line.replace(v, newVocal)
        line = line.strip().lower()
        diccionario.append(line)

def buscarFaltasOrtograficas(file):
    contador = 0
    indice = 0
    lineasLeidas = 0
    archivosAbiertos = [open(nombreArchivoErrores[0], 'w'), open(nombreArchivoErrores[1], 'w'), open(nombreArchivoErrores[2], 'w')]

    file = open(file)
    for linea in file.readlines():
        lineasLeidas += 1
        if lineasLeidas % 500 == 0:
            print str(lineasLeidas)
        for palabra in palabrasOmitir:
            linea = linea.replace(palabra, "")
        linea = linea.strip()
        for palabra in linea.split():
            if palabra not in diccionario:
                contador += 1
                nuevaPalabra = '<b><u><font color="red">%s</font></u></b>' % (palabra) 
                linea = linea.replace(palabra, nuevaPalabra)
                archivosAbiertos[indice].write(linea + '<br>')
                indice = 0 if indice == 2 else indice + 1
                break
    print "Se encontraron {} errores".format(contador)

if __name__ == '__main__':
    #Lleva control de tiempos
    handler = logging.StreamHandler()
    handler.setFormatter(ElapsedFormatter())
    logging.getLogger().addHandler(handler)

    log = logging.getLogger('test')
    log.error("Inicio de detecciones de errores")

    cargarDiccionario(nombreDiccionario)
    buscarFaltasOrtograficas(archivoOrigen)

    log.error("Fin de detecciones de errores")