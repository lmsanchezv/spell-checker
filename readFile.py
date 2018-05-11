#!/usr/bin/python
import sys,string,re,os
import multiprocessing as mp


url_regex = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\[\]]+|\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\))+(?:\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)|[^\s`!(){};:'".,<>?\[\]]))""")
archivoOrigen = "datos_original_mitad.txt"
archivoDestino = "output5.txt"
matches = []
contador = 0
palabrasModificadas = []

def procesar_match(m):
    matches.append(m.group(0))
    return '{{URL}}'

def procesar(line):
    global contador,palabrasModificadas
    print contador
    try:
        contador += 1
        if contador % 500 == 0:
            print str(contador)
        #quita caracteres en blanco al principio y final
        lineaLimpia = line.strip()   
        #quitar URLs
        lineaLimpia = url_regex.sub(procesar_match, lineaLimpia)
        #quitar números
        lineaLimpia = re.sub("\d+", "xxNumxx", lineaLimpia)

        palabras = lineaLimpia.split()
        for r, palabra in enumerate(palabras):
            if r == 0:
                #si es la primer palabra, le concatene el inicio de oración
                palabrasModificadas = (palabrasModificadas + ['<s> '])
            #quita puntuaciones
            palabra = palabra.translate(string.maketrans("",""), string.punctuation).lower()
            #agregar palabra a la lista de palabras modificadas
            palabrasModificadas = palabrasModificadas + [palabra + ' ']
        #al final de la oración agregar un cierre de oración
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
            print "procesando %s" % (line)
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

def readFile(file):
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
    procesarFileMultipleJobs()