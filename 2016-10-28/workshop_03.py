
# coding: utf-8

# # L Shaped Stair

# ![image1](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/6c069717de094fd68ba6cf0b276a4dd4.jpg)
# 
# ![image2](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/LS_01.gif)
# 
# ![image3](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/l shape.gif)

# ## Procedimento di calcolo del numero di gradini,  alzata e pedana
# 
# 1. Prendere l'atezza del dislivello;
# 2. Calcolare il numero di scalini: altezza in cm / 18 cm = scalini e questo numero arrotondato per eccesso;
# 3. Calcolare l'altezza della alzata: altezza in cm / scalini = alzata cm;
# 4. Estensione della pedana: 64 cm - 2 * (alzata cm).
# 
# Considerazioni generiche:
# - L'alzata non può essere superiore a 18 cm né la pedata minore di 28 cm;
# - Normalmente al massimo ogni 9 0 10 gradini deve essere disposto un pianerottolo di profondità ≥ alla larghezza della rampa. 
# - Abitazioni individuali dovranno avere una larghezza di almeno 0,80 m.

# In[1]:

from pyplasm import *
from math import *


# ## Funzione di generazione scale
# 
# La funzioen ggpl_l_shaped_stair genera come la scala anche come input le dimensione del vano scala. Questa funzione si basa sull'utilizzo di alcune sotto-funzioni base:
# - **makeStep**: Questa funzione avendo come input la pedata, l'alzata e un booleano che indica se il gradino che deve essere generato è l'ultimo della scalina
# ```
# def makeStep(tread, riser, last):
#         if (last):
#             return CUBOID([1, tread, riser])
#         else:
#             base = MKPOL([[[0, 0], [0, riser], [tread, riser], [2 * tread, riser], [tread, 0]], [[1, 2, 3, 4, 5]], 1])
#             base = PROD([base, QUOTE([1])])
# 
#             return STRUCT([
#                 R([1, 3])(-math.pi / 2),
#                 R([1, 2])(-3 * math.pi / 2),
#                 base
#             ])
# ```
# - **stairValue**: Questa funzione avendo come input l'altezza del vano scale genera i parametri base che servono per costruire la scala. Infatti questa funzione ha come output una tripletta di elementi dove il primo è intero corrispondente al numero di gradini, il secondo è un float che corrisponde all'alzata e l'ultimo è un floato che corrisponde alla pedata. 
# ```
#  def stairValue(dz):
#         step = math.floor(dz * 100 / 18) + 1
#         riser = dz * 100 / step
#         tread = 64 - 2 * riser
# 
#         return [int(step), riser / 100, tread / 100]
# ```
# - **makeStair**: Questa funzione creata la scala utilizzando la funzione **makeStep** avendo come parametri in ingresso il numero di gradini, la pedata e l'alzato.
# ```
#  def makeStair(step, riser, tread):
#         steps = []
#         for i in range(step):
#             if i != 0:
#                 steps.append(T([2, 3])([tread, riser]))
#             steps.append(makeStep(tread, riser, i == step - 1))
# 
#         return steps
# ```
# 
# ## Funzionamento di generazione della L sulla scala
# 
# La generazioen della L sulla scala avviene nel seguente modo:
# ```
#  step, riser, tread = stairValue(dz)
#     stairs = []
#     stay_on_x = True
#     way = 0
# 
#     while step != 0:
#         length = dx if stay_on_x else dy
# 
#         offset = 2 if stay_on_x and way != 2 else (3 if stay_on_x else 1)
# 
#         possible = int(math.floor((length - offset) / tread))
# 
#         if possible >= step:
#             stairs.extend(makeStair(step, riser, tread))
#             step = 0
#         else:
#             step -= possible
#             stairs.extend(makeStair(possible, riser, tread))
#             stairs.append(T([2])([tread]))
# 
#             stairs.append(CUBOID([1 + tread, 1, riser]))
#             stairs.append(T(2 if stay_on_x else 1)(1))
#             stairs.append(T(1 if stay_on_x else 2)(1))
#             stairs.append(R([1, 2])(- math.pi / 2.0))
#             stairs.append(T(3)(riser))
# 
#             stay_on_x = not stay_on_x
#             way += 1 if way != 2 else 0
# 
# ```
# 
# 1. Considero l'asse x come asse di riferimento
# 2. Determino il numero di scalini possibili su questo asse in base alla grandella del vano scape sull'asse di riferimento
# 3. Se il numero di gradini disponibili è maggiore di quelli possibili allora creo la rampa di scale e finisco l'algoritmo
# 4. Altrimenti creo la scala utilizzando come numero di gradini il numero di possibili gradini su quell'asse.
# 5. Creo il pianerottolo
# 6. Faccio una rotazione di - 90° sull'asse di riferimento
# 7. Sottraggo al numero di scalani totali il numero di scalini utilizzati in questa rampa
# 8. Ricomincio dal passo 2 cambiando asse di riferimento alternando x a y e viceversa

# In[5]:

""" ggpl_l_shaped_stair

Questa funzione genera una scala a L avendo come parametro le dimensioni x, y e z del vano scale

@param dx: la larghezza del vano scale
@param dy: la lunghezza del vano scale
@param dz: l'altezza del vano scale
@return: La scala.
"""
def ggpl_l_shaped_stair(dx, dy, dz):
    """ makeStep 
    
    Questa funzione avendo come input la pedata, l'alzata e un booleano che indica se il gradino che deve essere generato è l'ultimo della scalina
    
    @param tread: la dimensione della pedata dello scalino
    @param riser: l'alzata dello scalino
    @param last: un booleano che indica se il gradino che deve essere generato è l'ultimo della scalina
    @param: il gradino che si è generato dai dati di input
    """
    def makeStep(tread, riser, last):
        if (last):
            return CUBOID([1, tread, riser])
        else:
            base = MKPOL([[[0, 0], [0, riser], [tread, riser], [2 * tread, riser], [tread, 0]], [[1, 2, 3, 4, 5]], 1])
            base = PROD([base, QUOTE([1])])

            return STRUCT([
                R([1, 3])(-math.pi / 2),
                R([1, 2])(-3 * math.pi / 2),
                base
            ])

    """ stairValue
    
    Questa funzione avendo come input l'altezza del vano scale genera i parametri base che servono per costruire la scala. Infatti questa funzione ha come output una tripletta di elementi dove il primo è intero corrispondente al numero di gradini, il secondo è un float che corrisponde all'alzata e l'ultimo è un floato che corrisponde alla pedata. 
    
    @param dz: l'altezza del vano scale
    @return: i paramentri base per la costruzione della scala
    """
    def stairValue(dz):
        step = math.floor(dz * 100 / 18) + 1
        riser = dz * 100 / step
        tread = 64 - 2 * riser

        return [int(step), riser / 100, tread / 100]

    """ makeStair
    
    Questa funzione creata la scala utilizzando la funzione **makeStep** avendo come parametri in ingresso il numero di gradini, la pedata e l'alzato.
    
    @param step: un intero che indica il numero di gradini
    @param riser: un float ch indica l'alzata dello scalino
    @param tread: un float che indiica la dimensione della pedata dello scalino
    @return: la scalinata
    """
    def makeStair(step, riser, tread):
        steps = []
        for i in range(step):
            if i != 0:
                steps.append(T([2, 3])([tread, riser]))
            steps.append(makeStep(tread, riser, i == step - 1))

        return steps

    step, riser, tread = stairValue(dz)
    stairs = []
    stay_on_x = True
    way = 0

    while step != 0:
        length = dx if stay_on_x else dy

        offset = 2 if stay_on_x and way != 2 else (3 if stay_on_x else 1)

        possible = int(math.floor((length - offset) / tread))

        if possible >= step:
            stairs.extend(makeStair(step, riser, tread))
            step = 0
        else:
            step -= possible
            stairs.extend(makeStair(possible, riser, tread))
            stairs.append(T([2])([tread]))

            stairs.append(CUBOID([1 + tread, 1, riser]))
            stairs.append(T(2 if stay_on_x else 1)(1))
            stairs.append(T(1 if stay_on_x else 2)(1))
            stairs.append(R([1, 2])(- math.pi / 2.0))
            stairs.append(T(3)(riser))

            stay_on_x = not stay_on_x
            way += 1 if way != 2 else 0

    return STRUCT(stairs)


# In[6]:

stair = ggpl_l_shaped_stair(4,3,10)
print SIZE([1,2,3])(stair)

VIEW(stair)


# ## Esempi di esecuzione
# 
# ### Esempio 1
# ![example1_original](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/LS_01.gif)
# 
# ```
# VIEW(ggpl_l_shaped_stair(4,3,10))
# ```
# 
# ![example1_render](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/example/example1.png)
# ### Esempio 2
# 
# ![example2_original](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/Jyvaskyla_tower_stairs.jpg)
# 
# ```
# VIEW(ggpl_l_shaped_stair(4,3,30))
# ```
# 
# ![example2_render1](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/example/example2.1.png)
# 
# ![example2_render1](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-10-28/images/example/example2.2.png)
# 

# # Link Utili
# - [Come calcolare una scala](http://www.uncome.it/casa/articolo/come-calcolare-una-scala-341.html)

# In[ ]:



