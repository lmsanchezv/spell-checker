import math
import re,os

# Usado para palabras que no existen en el vocabulario de entrenamiento
UNK = None
# inicio y fin de oracion
inicioOracion = "<s>"
finOracion = "</s>"

def leerOracionesArchivo(rutaArchivo):
    with open(rutaArchivo, "r") as f:
        return [re.split("\s+", line.rstrip('\n')) for line in f]

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

# Calcular cantidad de unigramas y bigramas
def calcularNumeroUnigramas(oraciones):
    cuentaUnigramas = 0
    for oracion in oraciones:
        # Quitar dos por los <s> y </s>
        cuentaUnigramas += len(oracion) - 2
    return cuentaUnigramas

def calcularNumeroBigramas(oraciones):
    cuentaBigramas = 0
    for oracion in oraciones:
        # Quitar unor por el numero de bigramas en la oracion
        cuentaBigramas += len(oracion) - 1
    return cuentaBigramas

# calcular probabilidad de unigramas
def imprimirProbabilidadUnigramas(llavesVocabulario, modelo, fileName):
    with open(fileName, 'a') as f:
        contador = 0
        for llave in llavesVocabulario:
            contador += 1
            if contador % 500 == 0:
                print "{} unigramas analizados".format(contador)
            if llave != inicioOracion and llave != finOracion:
                valorImprimir = "{},{}".format(llave if llave != UNK else "UNK", modelo.calcularProbabilidadUnigrama(llave))
                f.write(valorImprimir + "\n")
        print("")

# calcular probabilidad de bigramas
def imprimirProbabilidadBigramas(llavesVocabulario, modelo, fileName):
    print "\t\t",
    with open(fileName, 'a') as f:
        #for llave in llavesVocabulario:
        #    if llave != inicioOracion:
        #        print(llave if llave != UNK else "UNK" + "\t\t")
        #print("")
        contador = 0
        for llave in llavesVocabulario:
            if llave != finOracion:
                print(llave if llave != UNK else "UNK" + "\t\t")
                for segundaLlave in llavesVocabulario:
                    if segundaLlave != inicioOracion:
                        contador += 1
                        if contador % 1000 == 0:
                            print "{} bigramas analizados".format(contador)
                        print(segundaLlave if segundaLlave != UNK else "UNK" + "\t\t")
                        print("{0:.5f}".format(modelo.calcularProbabilidadBigrama(llave, segundaLlave)) + "\t\t")
                        valorImprimir = "{},{},{}".format(llave if llave != UNK else "UNK", segundaLlave if segundaLlave != UNK else "UNK", modelo.calcularProbabilidadBigrama(llave, segundaLlave))
                        f.write(valorImprimir + "\n")
                print("")
        print("")

# calculate perplexty
def calcularPerplejidadUnigramas(modelo, oraciones):
    cuentaUnigramas = calcularNumeroUnigramas(oraciones)
    probabilidadLogOracion = 0
    for oracion in oraciones:
        try:
            probabilidadLogOracion -= math.log(modelo.calcularProbabilidadOracion(oracion), 2)
        except:
            probabilidadLogOracion -= float('-inf')
    return math.pow(2, probabilidadLogOracion / cuentaUnigramas)

def calcularPerplejidadBigramas(modelo, oraciones):
    numeroBigrmas = calcularNumeroBigramas(oraciones)
    probabilidadLogOracion = 0
    for oracion in oraciones:
        try:
            probabilidadLogOracion -= math.log(modelo.calcularProbabilidadOracionBigrama(oracion), 2)
        except:
            probabilidadLogOracion -= float('-inf')
    return math.pow(2, probabilidadLogOracion / numeroBigrmas)