# coding: utf-8

# In[7]:

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
# - Pavimento Interno
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Pavimento Interno.png)
#
# - Pavimento Esterno
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Pavimento Esterno.png)
#
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

# In[8]:

def createStructFromLines(file_name, size):
    """createStructFromLines

    Metodo che serve a creare la struttura 2D rappresentata dal file passato come parametro

    :param file_name: Il filename del file delle linee della struttura
    :param size: Lo spessore della struttura
    :return: HPC della struttura
    """

    points = []
    #: L'insieme dei punti che costituiscono la struttura

    indexs = []
    #: La coppia di indici che costituiscono le varie parti della struttura

    i = 0
    #: Ultimo indice aggiunto

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

# In[9]:

def createFloorFromLines(file_name):
    """ createFloorFromLines

    Metodo per la creazione del pavimento della struttura passata come paramentro rappresentato dal file file_name

    :param file_name:  Il filename del file delle linee della struttura
    :return: HPC del pavimento
    """

    points = []
    #: L'insieme dei punti che costituiscono la struttura

    indexs = []
    #: L'insieme di tutti i punti della struttura

    i = 0
    #: Ultimo indice aggiunto

    with open(file_name, 'rb') as csvfile:
        builderreader = csv.reader(csvfile)

        for row in builderreader:
            points.append([float(row[0]), float(row[1])])
            points.append([float(row[2]), float(row[3])])
            i += 2
            indexs.extend([i - 1, i])

    return MKPOL([
        points,
        [indexs],
        None
    ])


# ## Definizione Modelli

# In[10]:

externalWall = createStructFromLines("pianimetria/lines/Muro Esterno.lines", 4)
#: Il muro esterno della casa

internalWall = createStructFromLines("pianimetria/lines/Strutture interne.lines", 3)
#: Le mura interne della casa

windows = createStructFromLines("pianimetria/lines/Finestre.lines", 8)
#: Le finestre della casa

doors = createStructFromLines("pianimetria/lines/Porte.lines", 8)
#: Le porte della casata

pillars = createStructFromLines("pianimetria/lines/Colonne Interne.lines", 5)
#: Le colonne portanti interne delle case

balconies_original = createStructFromLines("pianimetria/lines/Terrazzi.lines", 4)
#: I balconi della casa

floor_internal = STRUCT([
    createFloorFromLines("pianimetria/lines/Pavimento Parte 1.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 2.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 3.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 4.lines")
])
#: Il pavimento interno alla casa

floor_balcony = STRUCT([
    createFloorFromLines("pianimetria/lines/Pavimento Parte 5.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 6.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 7.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 8.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 9.lines"),
    createFloorFromLines("pianimetria/lines/Pavimento Parte 10.lines")
])
#: Il pavimento esterno alla casa, percui il pavimento nei balconi


# ## Parti finali della casa

# In[13]:

external = PROD([
    DIFF([
        externalWall,
        windows,
        doors
    ]),
    QUOTE([100])
])
#: Questa variabile rappresenta le mura esterne con le fessure per le finestre

internal = PROD([
    DIFF([
        internalWall,
        windows,
        doors
    ]),
    QUOTE([100])
])
#: Questa variabile rappresenta le mura interne con le fessure per le porte e per le finestre

pillars = PROD([
    pillars,
    QUOTE([100])
])
#: Pilastri in 3D

balconies = PROD([
    balconies_original,
    QUOTE([50])
])
#: Banconi in 3D


# ## Esempio 1 - Struttura base

# In[12]:

VIEW(STRUCT([
    COLOR(RED)(external),
    COLOR(BLUE)(internal),
    COLOR(GREEN)(pillars),
    COLOR(CYAN)(balconies),
    floor_internal,
    floor_balcony
]))

# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Esempio1.1.png)
#
# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Esempio1.2.png)

# ## Esempio 2 - Aggiunta texture

# In[ ]:

VIEW(STRUCT([
    COLOR(WHITE)(external),
    COLOR(WHITE)(internal),
    COLOR(WHITE)(pillars),
    COLOR(WHITE)(balconies),
    TEXTURE(["texture/parket.png", True, False, 1, 1, 0, 1, 1])(floor_internal),
    TEXTURE(["texture/cotto.png", True, False, 1, 1, 0, 1, 15])(floor_balcony)
]))


# ### Risultati

# ![pianimetria](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-12-02/image/Esempio2.png)
