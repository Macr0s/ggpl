
# coding: utf-8

# # Workshop 4 - Hip Roof
# 
# ![hip_roof](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/Rectangular-hip-roof.png)

# In[ ]:

from pyplasm import *


# ## Versione 1

# In[26]:

""" ggpl_hip_roof

Questa funzione prende in ingresso i dati del tetto divisi in due gruppi vertici e celle.

@param verts: i vertifici del tetto
@param cells: la cella del tetto
@return: il tetto

"""
def ggpl_hip_roof(verts, cells):
    roof = []
    
    """ makeRidge
    
    Questa funzione avendo in input i dati del tetto crea la copertura del tetto
    
    @param verts: i vertifici del tetto
    @param cells: la cella del tetto
    @return: la copertura del tetto
    
    """
    def makeRidge(verts, cells):
        remove=[]
        
        
        """ findFN
        
        Questa funzione verifica se il punto x ha come coordinata z un valore diverso da zero. Se il punto soddisfa 
        questa condizione allora viene inserito nella lista globale remove
        
        @param x: il punto da controllare
        @return: il punto pasato come parametro
        
        """        
        def findFN(x):
            if not x[2] == 0:
                remove.append(x)
            return x
        
        """ removeFN
        
        Questa funzione serve per muovere i punti interni alla struttura in alto cosi da creare la copertura del
        tetto
        
        @param x: il punto della struttura
        @return: il nuovo punto della struttura
        
        """
        def removeFN(x):
            for i in range(len(remove)):
                y = remove[i]
                if y[0] == x[0] and y[1] == x[1] and x[2] == 0:
                    return y
            return x

        ridge = OFFSET([0.1, 0.2, 0.1])((MKPOL([
            map(removeFN, map(findFN, verts)),
            cells,
            None
        ])))

        return STRUCT([
            T(3)(0.1),
            ridge
        ])
    
    """ makeStructure
    
    Questa funzione avendo come input i dati del tetto crea la struttura portante del tetto stesso
    
    @param verts: i vertifici del tetto
    @param cells: la cella del tetto
    @return: la struttura portante del tetto
    
    """
    def makeStructure(verts, cells):
        return OFFSET([0.1, 0.2, 0.1])(SKEL_1(MKPOL([verts,cells,None])))

    ridge = makeRidge(verts, cells)
    struct = makeStructure(verts, cells)

    roof.append(COLOR(RED)(ridge))
    roof.append(struct)
    return STRUCT(roof)


# ### Esempio 1

# In[27]:

VIEW(ggpl_hip_roof([
    [0,0,0],[0,10,0],[5,5,0],[5,5,5],[15,0,0],[15,10,0],[10,5,0],[10,5,5]
],
[
    [3,4,2,1],[8,5,6,7],[5,8,7,3,4,1],[2,4,3,7,8,6]
]))


# #### Risultato
# 
# ![example1.1](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example1.1.png)
# 
# ![example1.2](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example1.2.png)

# ### Esempio 2

# In[28]:

VIEW(ggpl_hip_roof([
        [0, 10, 0], [4, 10, 0], [2, 8, 0], [2, 2, 0], [2, 8, 4], [2, 2, 4],
        [4, 4, 0], [0, 0, 0], [10, 0, 0], [10, 4, 0], [8, 2, 0], [8, 2, 4]
],[
        [1, 2, 3, 5],
        [1, 8, 4, 3, 5, 6], 
        [2, 7, 6, 5, 3, 4],
        [8, 9, 11, 4, 6, 12],
        [9, 10, 11, 12],
        [7, 10, 11, 4, 6, 12]
]))


# #### Risultato
# 
# ![example2.1](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example2.1.png)
# 
# ![example2.2](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example2.2.png)
# 
# ![example2.3](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example2.3.png)

# ## Versione 2

# In[14]:

def ggpl_hip_roof_hpc(struct):
    
    """ cleanUKPOL
    
    Questa funzioen serve per determinare i vertici e le celle da un hpc
    
    @param skel: l'HPC in questione
    @return: una lista di due elementi che corrisponde uno ai vertici e l'altro alle celle
    
    """
    def cleanUKPOL(skel):
        points, cells, none = UKPOL(skel)
        
        """ roundFN
        
        Questa funzione prende in input un punto dello spazio e lo arrotonda al punto con coordinate intere
        
        @param x: il punto da arrotondare
        @return: il nuovo punto arrotondato
        
        """
        def roundFN(x):
            return [round(x[0]), round(x[1]), round(x[2])]

        points = map(roundFN, points)

        point_dict = {}

        for i in range(len(points)):
            key = ''.join(str(e) for e in points[i])

            if (point_dict.has_key(key)):
                point_dict[key][0] += 1
                point_dict[key][2].append(i)
            else:
                point_dict[key] = [
                    1,
                    i + 1,
                    [],
                    points[i]
                ]

        points_new = []
        support = []
        for value in point_dict.values():
            points_new.append(value[3])

            for i in range(len(value[2])):
                support.append([value[1], value[2][i]])
        
        """ iterateFN
        
        Questa funzione corregge la cella x
        
        @param x: la cella con gli indici sbagliati
        @return: la cella corretta
        
        """
        def iterateFN(x):
            
            """ replace
            
            Questa funzione verifica se l'elemento y della cella è corretto e se non lo è allora lo corregge
            
            @param y: l'elemento della cella
            @return: l'elemento della cella corretto
            
            """
            def replace (y):
                for i in range(len(support)):
                    if support[i][1] == y:
                        return support[i][0]
                return y

            return map(replace, x)

        cells_new = map(iterateFN, cells)

        return [points, cells_new]
    
     """ makeRidge
    
    Questa funzione avendo in input i dati del tetto crea la copertura del tetto
    
    @param verts: i vertifici del tetto
    @param cells: la cella del tetto
    @return: la copertura del tetto
    
    """
    def makeRidge(verts, cells):
        remove = []
        
        
        """ findFN
        
        Questa funzione verifica se il punto x ha come coordinata z un valore diverso da zero. Se il punto soddisfa 
        questa condizione allora viene inserito nella lista globale remove
        
        @param x: il punto da controllare
        @return: il punto pasato come parametro
        
        """
        def findFN(x):
            if not x[2] == 0:
                remove.append(x)
            return x
        
        """ removeFN
        
        Questa funzione serve per muovere i punti interni alla struttura in alto cosi da creare la copertura del
        tetto
        
        @param x: il punto della struttura
        @return: il nuovo punto della struttura
        
        """
        def removeFN(x):
            for i in range(len(remove)):
                y = remove[i]
                if y[0] == x[0] and y[1] == x[1] and x[2] == 0:
                    return y
            return x

        ridge = OFFSET([0.1, 0.2, 0.1])((MKPOL([
            map(removeFN, map(findFN, verts)),
            cells,
            None
        ])))

        return STRUCT([
            T(3)(0.1),
            ridge
        ])

    verts, cells = cleanUKPOL(struct)

    roof = []
    ridge = makeRidge(verts, cells)
    struct = OFFSET([0.1, 0.2, 0.1])(SKEL_1(struct))

    roof.append(COLOR(RED)(ridge))
    roof.append(struct)
    return STRUCT(roof)


# ### Esempio 1

# In[29]:

VIEW(ggpl_hip_roof_hpc(MKPOL([
    [
        [0,0,0],[0,10,0],[5,5,0],[5,5,5],[15,0,0],[15,10,0],[10,5,0],[10,5,5]
    ],
    [
        [3,4,2,1],[8,5,6,7],[5,8,7,3,4,1],[2,4,3,7,8,6]
    ],
    None
])))


# #### Risultato
# 
# ![example3.1](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example3.1.png)
# 
# ![example3.2](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example3.2.png)
# 
# ![example3.3](https://raw.githubusercontent.com/Macr0s/ggpl/master/2016-11-04/images/example3.3.png)
