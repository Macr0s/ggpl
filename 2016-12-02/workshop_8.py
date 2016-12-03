
# coding: utf-8

# In[1]:

from pyplasm import *
import csv


# # Modellazione di una pianimetria di una casa
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Pianimetria.png)
#
# La pianimetria riportata in figura rappresenta il modello di riferimento per la realizzazione finale. Il software deve prendere dei files lines come input per la creazione delle varie parti della struttura. Questi file sono generati attraverso un tool online da file svg creati attraverso un programma di grafica vettoria che ha permesso di ricalcare la varie porti.
#
# Per far funzionare il programma si è voluto dividere la struttura nelle varie parti:
#
# - Mura esterne
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Muro Esterno.png)
#
# - Muri interni
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Strutture interne.png)
#
# - Colonne portanti
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Colonne interne.png)
#
# - Finestre
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Finestre.png)
#
# - Porte
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Porte.png)
#
# - Terrazzo
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Pianimetria.png)
#
# Considerando tutti questi livelli insieme otteniamo:
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Tutti insieme.png)
#
# Per generare il modello corrispondente viene creato attraverso l'utilizzo di due funzioni principali.
#
# 1. createStructFromLines: Crea le mura corrispondente a quella parte attraverso una creazione di una polilyne
#
# 2. createFloorFromLines: Crea il contorno del pavimento della zona rappresentata dal file passato come parametro

# ## Funzione 1: Creazione Muri

# In[5]:

def createStructFromLines(file_name, size):
    points = []
    indexs = []
    i = 0

    with open(file_name, 'rb') as csvfile:
        buildereader = csv.reader(csvfile)

        for row in buildereader:
            points.append([float(row[0]), float(row[1])])
            points.append([float(row[2]), float(row[3])])
            i += 2
            indexs.append([i - 1, i])

    return OFFSET([size, size])(
        MKPOL([
            points,
            indexs,
            None
        ])
    )


# ## Funzione 2: Creazione pavimento

# In[6]:

def createFloorFromLines(file_name, size):
    points = []
    indexs = []
    i = 0

    with open(file_name, 'rb') as csvfile:
        builderreader = csv.reader(csvfile)

        for row in builderreader:
            points.append([float(row[0]), float(row[1])])
            points.append([float(row[2]), float(row[3])])
            i += 2
            indexs.extend([i - 1, i])

    return OFFSET([size, size])(
        MKPOL([
            points,
            [indexs],
            None
        ])
    )


# ## Corpo centrale di unione delle varie parti

# In[4]:

if __name__ == "__main__":
    externalWall = createStructFromLines("pianimetria/lines/Muro Esterno.lines", 4)
    internalWall = createStructFromLines("pianimetria/lines/Strutture interne.lines", 4)
    windows = createStructFromLines("pianimetria/lines/Finestre.lines", 6)
    doors = createStructFromLines("pianimetria/lines/Porte.lines", 6)
    pillars = createStructFromLines("pianimetria/lines/Colonne Interne.lines", 4)
    balconies = createStructFromLines("pianimetria/lines/Terrazzi.lines", 4)
    internalFloor = createFloorFromLines("pianimetria/lines/Muro Esterno.lines", 4)
    floar1 = createFloorFromLines("pianimetria/lines/Pavimento Parte 1.lines", 4)
    floar2 = createFloorFromLines("pianimetria/lines/Pavimento Parte 2.lines", 4)
    floar3 = createFloorFromLines("pianimetria/lines/Pavimento Parte 3.lines", 4)

    external = DIFF([
        externalWall,
        windows,
        doors
    ])

    internal = DIFF([
        internalWall,
        windows,
        doors
    ])

    VIEW(STRUCT([
        COLOR(RED)(PROD([
            external,
            QUOTE([100])
        ])),
        COLOR(BLUE)(PROD([
            internal,
            QUOTE([100])
        ])),
        pillars,
        balconies,
        floar1,
        floar2,
        floar3
    ]))



# ## Risultato Finale

# In[ ]:



