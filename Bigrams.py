import math
from Unigrams import UnigramaModeloLenguaje

# oracion start and end
inicioOracion = "<s>"
finOracion = "</s>"

class BigramaModeloLenguaje(UnigramaModeloLenguaje):
    def __init__(self, oraciones, smoothing=False):
        UnigramaModeloLenguaje.__init__(self, oraciones, smoothing)
        self.frecuenciasBigramas = dict()
        self.bigramasUnicos = set()
        for oracion in oraciones:
            palabraAnterior = None
            for palabra in oracion:
                if palabraAnterior != None:
                    self.frecuenciasBigramas[(palabraAnterior, palabra)] = self.frecuenciasBigramas.get((palabraAnterior, palabra), 0) + 1
                    if palabraAnterior != inicioOracion and palabra != finOracion:
                        self.bigramasUnicos.add((palabraAnterior, palabra))
                palabraAnterior = palabra
        self.palabrasUnicasBigrama = len(self.frecuenciasUnigramas)

    def calcularProbabilidadBigrama(self, palabraAnterior, palabra):
        numeradorProbabilidadPalabraBigrama = self.frecuenciasBigramas.get((palabraAnterior, palabra), 0)
        denominadorProbabilidadPalabraBigrama = self.frecuenciasUnigramas.get(palabraAnterior, 0)
        if self.smoothing:
            numeradorProbabilidadPalabraBigrama += 1
            denominadorProbabilidadPalabraBigrama += self.palabrasUnicasBigrama
        return 0.0 if numeradorProbabilidadPalabraBigrama == 0 or denominadorProbabilidadPalabraBigrama == 0 else float(
            numeradorProbabilidadPalabraBigrama) / float(denominadorProbabilidadPalabraBigrama) * 100

    def calcularProbabilidadOracionBigrama(self, oracion, normalizarProbabilidad=True):
        probabilidadLogOracion = 0
        palabraAnterior = None
        for palabra in oracion:
            if palabraAnterior != None:
                probabilildadPalabra = self.calcularProbabilidadBigrama(palabraAnterior, palabra)
                probabilidadLogOracion += math.log(probabilildadPalabra, 2)
            palabraAnterior = palabra
        return (math.pow(2, probabilidadLogOracion) if normalizarProbabilidad else probabilidadLogOracion) * 100
