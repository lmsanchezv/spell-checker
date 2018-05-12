import multiprocessing as mp,re
from os import remove, path
from Bigrams import BigramaModeloLenguaje
from ModelsHelper import imprimirProbabilidadUnigramas, imprimirProbabilidadBigramas,calcularPerplejidadUnigramas,calcularPerplejidadBigramas,chunkify
from ElapsedTimeFormatter import ElapsedFormatter
import logging

#input file to create the LangModel
archivoOrigen = "output.txt"

def procesarBigramasUnigramas(chuckSentnces):
    dataset = chuckSentnces
    datasetPruebas = chuckSentnces
    
    modeloSinSmoothing = BigramaModeloLenguaje(dataset)
    modeloConSmoothing = BigramaModeloLenguaje(dataset, smoothing=True)

    llavesVocabularioOrdenado = modeloSinSmoothing.obtenerVocabularioOrdenado()

    print("---------------- Dataset ---------------\n")
    print("=== UNIGRAMAS ===")
    print("- Sin smoothing  -")
    imprimirProbabilidadUnigramas(llavesVocabularioOrdenado, modeloSinSmoothing, 'unigramas.txt')
    print("\n- Con smoothing  -")
    imprimirProbabilidadUnigramas(llavesVocabularioOrdenado, modeloConSmoothing, 'unigramas smoothed.txt')

    print("")

    print("=== BIGRAMAS ===")
    imprimirProbabilidadBigramas(llavesVocabularioOrdenado, modeloConSmoothing, 'bigramas smoothed.txt')

    print("")

    print("== PROBABILIDAD DE ORACIONES == ")
    lenOracionMasLarga = max([len(" ".join(oracion)) for oracion in datasetPruebas]) + 5
    print("sent", " " * (lenOracionMasLarga - len("sent") - 2), "uprob\t\tbiprob")
    for oracion in datasetPruebas:
        oracion_string = " ".join(oracion)
        print(oracion_string + " " * (lenOracionMasLarga - len(oracion_string)))
        print("{0:.5f}".format(modeloConSmoothing.calcularProbabilidadOracion(oracion)) + "\t\t")
        print("{0:.5f}".format(modeloConSmoothing.calcularProbabilidadOracionBigrama(oracion)))        
        
    print("")

    print("== PRUEBA PERPLEJIDAD == ")
    print("unigramas: ", calcularPerplejidadUnigramas(modeloConSmoothing, datasetPruebas))
    print("bigramas: ", calcularPerplejidadBigramas(modeloConSmoothing, datasetPruebas))
    
    print("")

def process_wrapper(chunkStart, chunkSize):
    with open(archivoOrigen) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        procesarBigramasUnigramas([re.split("\s+", line.rstrip('\n')) for line in lines])

def processMultipleThreads():
    print "================="
    print "Proceso iniciado"
    #init objects
    if path.isfile('unigramas.txt'):
        remove('unigramas.txt')
    if path.isfile('unigramas smoothed.txt'):
        remove('unigramas smoothed.txt')
    if path.isfile('bigramas smoothed.txt'):
        remove('bigramas smoothed.txt')
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    jobs = []
    #create jobs
    for chunkStart,chunkSize in chunkify(archivoOrigen):
        jobs.append(pool.apply_async(process_wrapper,(chunkStart,chunkSize)))

    #wait for all jobs to finish
    for job in jobs:
        job.get()
    print "================="
    print "Proceso completado"
    pool.close()

if __name__ == '__main__':
    #Lleva control de tiempos
    handler = logging.StreamHandler()
    handler.setFormatter(ElapsedFormatter())
    logging.getLogger().addHandler(handler)

    log = logging.getLogger('test')
    log.error("Inicio de creacion de modelos")

    processMultipleThreads()

    log.error("Fin de creacion de modelos")
