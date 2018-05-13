#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,string,re,os
import multiprocessing as mp
from ElapsedTimeFormatter import ElapsedFormatter
import logging, handleAccentuation as ha

url_regex = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\[\]]+|\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\))+(?:\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)|[^\s`!(){};:'".,<>?\[\]]))""")
archivoOrigen = "datos_original_mitad.txt"
archivoDestino = "output.txt"
matches = []
contador = 0
palabrasModificadas = []

def procesar_match(m):
    matches.append(m.group(0))
    return 'xxURLxx'

def procesar(line):
    global contador,palabrasModificadas
    try:
        contador += 1
        if contador % 500 == 0:
            print contador
        #quita caracteres en blanco al principio y final
        lineaLimpia = line.strip()   
        #quitar URLs
        lineaLimpia = url_regex.sub(procesar_match, lineaLimpia)
        #quitar numeros
        lineaLimpia = re.sub("\d+", "xxNumxx", lineaLimpia)

        palabras = lineaLimpia.split()
        for r, palabra in enumerate(palabras):
            if r == 0:
                #si es la primer palabra, le concatene el inicio de oracion
                palabrasModificadas = (palabrasModificadas + ['<s> '])
            #quita puntuaciones
            for v in ha.options:
                index = palabra.find(v)
                if index != -1:
                    newVocal = ha.options[v]()
                    palabra = palabra.replace(v, newVocal)
            palabra = palabra.translate(string.maketrans("",""), string.punctuation).lower()
            #agregar palabra a la lista de palabras modificadas
            palabrasModificadas = palabrasModificadas + [palabra + ' ']
        #al final de la oracion agregar un cierre de oracion
        palabrasModificadas = (palabrasModificadas + ['</s>'] + ['\n'])
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst           # __str__ allows args to be printed directly

def procesar_wrapper(chunkStart, chunkSize):
    with open(archivoOrigen) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            procesar(line)
        with open(archivoDestino, 'a') as f:
            for line in palabrasModificadas:
                f.write(line)

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname,'r') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

def cargarArchivo(file):
    file = open(file)
    for line in file.readlines():
        line = line.strip()
        print line

def procesarFileMultipleJobs():
    print "================="
    print "Procesamiento iniciado"
    #init objects
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    jobs = []
    #create jobs
    for chunkStart,chunkSize in chunkify(archivoOrigen):
        jobs.append(pool.apply_async(procesar_wrapper,(chunkStart,chunkSize)))

    #wait for all jobs to finish
    for job in jobs:
        job.get()
    print "================="
    print "Procesamiento completado"
    pool.close()

if __name__ == '__main__':
    #Lleva control de tiempos
    handler = logging.StreamHandler()
    handler.setFormatter(ElapsedFormatter())
    logging.getLogger().addHandler(handler)

    log = logging.getLogger('test')
    log.error("Inicio de creacion de modelos")

    if os.path.isfile(archivoDestino):
        os.remove(archivoDestino)
    procesarFileMultipleJobs()

    log.error("Fin de creacion de modelos")