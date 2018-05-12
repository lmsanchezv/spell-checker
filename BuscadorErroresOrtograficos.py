import os
from ElapsedTimeFormatter import ElapsedFormatter
import logging

nombreDiccionario = "diccionarioCompletoEspanolCR.txt"
nombreArchivoErrores = ["Errores1.txt","Errores2.txt","Errores3.txt"]
archivoOrigen = "output.txt"
palabrasOmitir = ["<s>","</s>","xxurlxx","xxnumxx"]

diccionario = []

def cargarDiccionario(file):
    file = open(file)
    for line in file.readlines():
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
        linea = linea.decode('utf-8-sig')
        for palabra in palabrasOmitir:
            linea = linea.replace(palabra, "")
        linea = linea.strip()
        for palabra in linea.split():
            if palabra not in diccionario:
                contador += 1
                archivosAbiertos[indice].write(linea + '\n\r')
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