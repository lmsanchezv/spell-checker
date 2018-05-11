import math

# Usado para palabras que no existen en el vocabulario de entrenamiento
UNK = None

# inicio y fin de oración
inicioOracion = "<s>"
finOracion = "</s>"

class UnigramaModeloLenguaje:
    def __init__(self, oraciones, smoothing=False):
        self.frecuenciasUnigramas = dict()
        self.tamanoCorpus = 0
        for oracion in oraciones:
            for palabra in oracion:
                self.frecuenciasUnigramas[palabra] = self.frecuenciasUnigramas.get(palabra, 0) + 1
                if palabra != inicioOracion and palabra != finOracion:
                    self.tamanoCorpus += 1
        # Resta 2 porque el diccionari ofrecuenciasUnigramas contiene valores de inicioOracion y finOracion
        self.palabrasUnicas = len(self.frecuenciasUnigramas) - 2
        self.smoothing = smoothing

    def calcularProbabilidadUnigrama(self, palabra):
            numeradorProbabilidadPalabra = self.frecuenciasUnigramas.get(palabra, 0)
            denominadorProbabilidadPalabra = self.tamanoCorpus
            if self.smoothing:
                numeradorProbabilidadPalabra += 1
                # agregar uno más al total de palabras vistas para el UNK
                denominadorProbabilidadPalabra += self.palabrasUnicas + 1
            return float(numeradorProbabilidadPalabra) / float(denominadorProbabilidadPalabra)

    def calcularProbabilidadOracion(self, oracion, normalizarProbabilidad=True):
        probabilidadLogOracion = 0
        for palabra in oracion:
            if palabra != inicioOracion and palabra != finOracion:
                palabra_probability = self.calcularProbabilidadUnigrama(palabra)
                probabilidadLogOracion += math.log(palabra_probability, 2)
        return math.pow(2, probabilidadLogOracion) if normalizarProbabilidad else probabilidadLogOracion                

    def obtenerVocabularioOrdenado(self):
        vocabularioCompleto = list(self.frecuenciasUnigramas.keys())
        vocabularioCompleto.remove(inicioOracion)
        vocabularioCompleto.remove(finOracion)
        vocabularioCompleto.sort()
        vocabularioCompleto.append(UNK)
        vocabularioCompleto.append(inicioOracion)
        vocabularioCompleto.append(finOracion)
        return vocabularioCompleto
