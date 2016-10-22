
# coding: utf-8

# # Workshop 2
# Creazione di un struttura in cemento armato da un file csv che rappresenta un modello prestabilito
# ![modello](http://www.tecnisoft.it/immagini/breve_nove.jpg)

# In[6]:

from pyplasm import *
import csv


# ## Algoritmo di creazione della parete dell'edificio
# 
# L'algoritmo si basa sul fatto che la parete può essere diriva in due tipi di strutture basi:
# - La struttura a forma di F creata dalla funzione __createFStruct__ . Questo tipo di struttura si ripete più volte per creare la struttura finale
# - La struttura a forma di I creata dalla funzione __createFinalStruct__ . Questo tipo di struttura viene eseguita una sola volta alla fine della creazione delle strutture a forma di F
# 

# In[7]:

""" ggpl_bone_structure

Questo metodo crea una struttura 3D partendo dai dati presenti sul file csv passato come parametro

@param file_name: il file csv con i dati della struttura
@returns: la struttura 
"""
def ggpl_bone_structure(file_name):
    
    """ planeStructure
    
    Questo metodo create la struttura base avendo come dati di imput la sezione dele travi, la sezione del pilastro,
     la distanza tra un pilastro e l'altro e l'alterzza di intersezione delle travi sui pilastri
     
     @param beanSection: una tupla (bx,bz) che contiene la dimensione delle travi
     @param pillarSection: una tupla (px,py) che contiene la dimensione dei pilastri
     @param distancePillars: una lista di distanze relative tra un pilastro e l'altro
     @param intersectHeights: una lista di altezze relative che indicano la distranza tra una trave e l'altra sull'asse x
     @returns: la struttura base, che corrisponde ad una parete dell'edificio
    """
    def planeStructure(beamSection, pillarSection, distancePillars, intersectHeights):
        fStructs = []
        
        """ createFinalStruct
        
        Questo metodo crea una pilastro senza travi
        
        @param startPoint: Il punto di intersezione del pilastro con la base del piano di lavoro
        @param height: L'altezza del pilastro
        @returns: Il pilastro
        """
        def createFinalStruct(startPoint, height):
            pillar = CUBOID([pillarSection[0], pillarSection[1], height])
            return STRUCT([T(2)(startPoint), pillar])

        """ createFStruct
        
        Questo metodo crea la struttura portante con il pilastro e le travi di riferimento
        
        @param startPoint: Il punto di intersezione del pilastro con la base del piano di lavoro
        @param height: L'altezza del pilastro
        @param lengthBeam: La lunghezza delle travi
        @returns: Il pilastro
        """
        def createFStruct(startPoint, height, lengthBeam):
            fStruct = []

            fStruct.append(createFinalStruct(startPoint, height))
            hPillar = 0
            for i in range(len(intersectHeights)):
                beam = CUBOID([beamSection[1], lengthBeam, beamSection[0]])
                hPillar += intersectHeights[i]
                fStruct.append(STRUCT([
                    T(3)(hPillar),
                    T(2)(pillarSection[1] + startPoint),
                    beam
                ]))
            return STRUCT(fStruct)

        height = SUM(intersectHeights) + beamSection[1]

        startDistance = 0
        for iterator in range(len(distancePillars)):
            fStructs.append(createFStruct(startDistance, height, distancePillars[iterator]))

            startDistance = startDistance + pillarSection[1] + distancePillars[iterator]

        fStructs.append(createFinalStruct(startDistance, height))

        return STRUCT(fStructs)
    
    """ createTrasversalBeam
    
    Questa funzione crea le travi di collegamento tra una parete e l'altra
    
    @param beanSection: una tupla (bx,bz) che contiene la dimensione delle travi
    @param pillarSection: una tupla (px,py) che contiene la dimensione dei pilastri
    @param distancePillars: una lista di distanze relative tra un pilastro e l'altro
    @param intersectHeights: una lista di altezze relative che indicano la distranza tra una trave e l'altra sull'asse x
    @returns: la struttura base, che corrisponde ad una parete dell'edificio
    """
    def createTrasversalBeam(distance, beamSection, pillarSection, distancePillars, intersectHeights):
        y = []
        for index in range(len(distancePillars)):
            y.append(pillarSection[1])
            y.append(- distancePillars[index])
        y.append(pillarSection[1])

        x = [
            - pillarSection[0],
            distance
        ]

        z = []
        for i in range(len(intersectHeights)):
            if i == 0:
                z.append(-intersectHeights[i])
            else:
                z.append(-intersectHeights[i] + beamSection[1])
            z.append(beamSection[1])

        return PROD([
                PROD([QUOTE(x), QUOTE(y)]),
                QUOTE(z)
        ])
    
    """ parseCSV
    
    Questo metodo prende in input un file_name che indica il file csv da parsare per avere le informazioni della struttura
    
    Argomenti:
        file_name (string): il file name del file csv
        
    Yields:
        transaction: il vettore di traslazione tra una parete e l'altra
        beanSection: una tupla (bx,bz) che contiene la dimensione delle travi
        pillarSection: una tupla (px,py) che contiene la dimensione dei pilastri
        distancePillars: una lista di distanze relative tra un pilastro e l'altro
        intersectHeights: una lista di altezze relative che indicano la distranza tra una trave e l'altra sull'asse x
    """
    def parseCSV(file_name):
        odd = True
        transaction = None
        with open(file_name, 'rb') as csvfile:
            builderreader = csv.reader(csvfile)

            for row in builderreader:
                if odd:
                    odd = False
                    transaction = [float(row[0]), float(row[1]), float(row[2])]
                else:
                    odd = True
                    beamSection = [float(row[0]), float(row[1])]
                    pillarSection = [float(row[2]), float(row[3])]

                    distancePillars = []
                    start_point = 5
                    finish_point = int(row[4]) + start_point
                    for index in range(start_point, finish_point):
                        distancePillars.append(int(row[index]))

                    intersectHeights = []
                    start_point = finish_point + 1
                    finish_point = int(row[finish_point]) + start_point
                    for index in range(start_point, finish_point):
                        intersectHeights.append(int(row[index]))

                    yield transaction, beamSection, pillarSection, distancePillars, intersectHeights

    frames = []
    for transaction, beamSection, pillarSection, distancePillars, intersectHeights in parseCSV(file_name):
        frames.append(T(2)(transaction[1]))

        if transaction[0] != 0:
            frames.append(
                createTrasversalBeam(
                    transaction[0], beamSection, pillarSection, distancePillars,intersectHeights
                )
            )

        frames.append(T([1, 3])([transaction[0], transaction[2]]))
        frames.append(
            planeStructure(beamSection, pillarSection, distancePillars, intersectHeights)
        )

    return STRUCT(frames)


# In[ ]:

VIEW(ggpl_bone_structure("./frame_data_457024.csv"))


# In[ ]:



