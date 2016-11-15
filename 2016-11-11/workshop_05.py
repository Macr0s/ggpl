
# coding: utf-8

# In[1]:

from pyplasm import *


# # Funziona base per i colori

# In[2]:


def intRGBColor(values):
    """ intRGBColor

    Metodo preso dal web per ottenere colori da RGB
    :param values: lista di tre interi RGB
    :return: Colore
    """

    return Color4f([values[0] / 255.0,
                    values[1] / 255.0,
                    values[2] / 255.0,
                    1.0])


# # Sedia

# In[7]:


def ggpl_chair(dx, dy, dz):
    """ ggpl_chair

    Metodo per la creazione di una sedia

    :param dx: occupazione della struttura nelle x
    :param dy: occupazione della struttura nelle y
    :param dz: occupazione della struttura nelle z
    :return: hpc della sedia
    """

    #: Larghezza della gamba della sedia
    depth_leg = 0.05 * dx

    #: Distance della gamba dal bordo della sedia
    distance_leg = 0.03 * dx

    #: Profondità del sedile della sedia
    depth_chair = 0.01 * dz

    #: Altezza delle cambe della sedia
    height_leg = 0.45 * dz

    def makeLeg(dx, dy, dz):
        """ makeLeg

        Metodo che crea le gambe della sedia

        :param dx: occupazione della struttura nelle x
        :param dy: occupazione della struttura nelle y
        :param dz: occupazione della struttura nelle z
        :return: hpc delle gambe della sedia
        """

        def baseChair(dx, dy, dz):
            """ baseChair

            Metodo che crea la struttura sotto il sedile della sedia
            :param dx: occupazione della struttura nelle x
            :param dy: occupazione della struttura nelle y
            :param dz: occupazione della struttura nelle z
            :return: hpc
            """

            #: Struttura esterna della struttura a contatto con il sedile
            first = PROD([
                PROD([
                    QUOTE([-distance_leg, dx - distance_leg * 2]),
                    QUOTE([-distance_leg, dy - distance_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])

            #: Struttura interna della struttura a contatto con il sedile
            second = PROD([
                PROD([
                    QUOTE([-distance_leg - depth_leg, dx - distance_leg * 2 - depth_leg * 2]),
                    QUOTE([-distance_leg - depth_leg, dy - distance_leg * 2 - depth_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])

            return DIFF([
                first, second
            ])

        #: Proiezione della gambe sull'asse x
        base_x = QUOTE([-distance_leg, depth_leg, - (dx - distance_leg * 2 - depth_leg * 2), depth_leg])

        #: Proiezione della gambe sull'asse y
        base_y = QUOTE([-distance_leg, depth_leg, - (dy - distance_leg * 2 - depth_leg * 2), depth_leg])

        #: Proiezione della gambe sull'asse z
        base_z = QUOTE([dz - depth_leg])

        return STRUCT([
            PROD([
                PROD([base_x, base_y]),
                base_z
            ]),
            baseChair(dx, dy, dz)
        ])

    return STRUCT([
        COLOR(BLACK)(makeLeg(dx, dy, height_leg)),
        T(3)(height_leg),
        COLOR(intRGBColor([215, 190, 157]))(CUBOID([dx, dy, depth_chair])),
        T(2)(dy - depth_chair),
        COLOR(intRGBColor([215, 190, 157]))(CUBOID([dx, depth_chair, dz - depth_chair - height_leg]))
    ])


# ## Esempio

# In[8]:

v = ggpl_chair(0.40, 0.40, 0.9)
print SIZE([1,2,3])(v)
VIEW(v)


# # Sedia con Braccioli

# In[9]:


def ggpl_chair_with_arm(dx, dy, dz):
    """ ggpl_chair_with_arm

    Metodo per la creazione della sedia con i braccioli

    :param dx: occupazione della struttura nelle x
    :param dy: occupazione della struttura nelle y
    :param dz: occupazione della struttura nelle z
    :return: hpc della sedia con i braccioli
    """

    #: Larghezza della gamba della sedia
    depth_leg = 0.05 * dx

    #: Distance della gamba dal bordo della sedia
    distance_leg = 0.03 * dx

    #: Altezza delle cambe della sedia
    height_leg = 0.45 * dz

    #: Sedia senza braccioli
    chair = ggpl_chair(dx - depth_leg * 4, dy, dz)

    def makeArm(dx, dy, dz, right=True):
        """ makeArm
        
        Metodo per la creazione dei braccioli della sedia
        :param dx: occupazione della struttura nelle x
        :param dy: occupazione della struttura nelle y
        :param dz: occupazione della struttura nelle z
        :param right: Parametro opzionale per indicare se si tratta il bracciolo sinistro o quello destro
        :return: hpc del bracciolo
        """
        def supportArm():
            """supportArm

            Metodo che crea i supporti per i graccioli della sedia

            :return: hpc
            """

            return COLOR(BLACK)(STRUCT([
                T([2,3])([distance_leg,height_leg - depth_leg]),
                CUBOID([depth_leg * 2 + distance_leg, depth_leg, depth_leg]),
                T([2])([dy - distance_leg * 2 - depth_leg]),
                CUBOID([depth_leg * 2 + distance_leg, depth_leg, depth_leg])
            ]))

        #: Struttura base dei braccioli
        base = [
            COLOR(BLACK)(PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([-distance_leg, depth_leg, - (dy - distance_leg * 2 - depth_leg * 2), depth_leg])
                ]),
                QUOTE([-height_leg, (dz - height_leg - depth_leg) * 0.5])
            ])),
            COLOR(intRGBColor([215, 190, 157]))(PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([-distance_leg, dy - distance_leg * 2])
                ]),
                QUOTE([- (height_leg + (dz - height_leg - depth_leg) * 0.5), depth_leg])
            ]))
        ]

        #: Struttura finale dei braccioli
        final = [supportArm()]

        if not right:
            final.append(T(1)(distance_leg + depth_leg))

        final.extend(base)

        return STRUCT(final)

    return STRUCT([
        makeArm(depth_leg, dy, dz),
        T(1)(depth_leg*2),
        chair,
        T(1)(dx - depth_leg * 4 - distance_leg),
        makeArm(depth_leg, dy, dz, False)
    ])


# ## Esempio

# In[10]:

v = ggpl_chair_with_arm(0.40, 0.40, 0.9)
print SIZE([1,2,3])(v)
VIEW(v)


# # Sedia con tavolino

# In[11]:


def ggpl_chair_with_desk(dx, dy, dz):
    """ ggpl_chair_with_desk

    Metodo che crea una sedia con il tavolino

    :param dx: occupazione della struttura nelle x
    :param dy: occupazione della struttura nelle y
    :param dz: occupazione della struttura nelle z
    :return: hcp della sedia con tavolino
    """

    #: Larghezza della gamba della sedia
    depth_leg = 0.05 * dx

    #: Distance della gamba dal bordo della sedia
    distance_leg = 0.03 * dx

    #: Altezza delle cambe della sedia
    height_leg = 0.45 * dz

    #: Stuttura della sedia base
    chair = ggpl_chair_with_arm(dx, dy * 0.7, dz)

    def makeDesk(dx, dy, dz):
        """ makeDesk

        Metodo che crea il tavolo

        :param dx: occupazione della struttura nelle x
        :param dy: occupazione della struttura nelle y
        :param dz: occupazione della struttura nelle z
        :return: hcp del tavolino

        """

        return STRUCT([
            COLOR(intRGBColor([215, 190, 157]))(PROD([
                PROD([
                    QUOTE([dx, 0]),
                    QUOTE([dy, 0])
                ]),
                QUOTE([- (height_leg + (dz - height_leg - depth_leg) * 0.5), depth_leg])
            ])),
            T([2, 3])([dy, height_leg + (dz - height_leg - depth_leg) * 0.5]),
            COLOR(BLACK)(CUBOID([depth_leg, distance_leg, depth_leg]))
        ])

    return STRUCT([
        makeDesk(dx * 0.75, dy * 0.3, dz),
        T(2)(dy * 0.3),
        chair
    ])


# ## Esempio

# In[12]:

v = ggpl_chair_with_desk(0.40, 0.40, 0.9)
print SIZE([1,2,3])(v)
VIEW(v)


# # Tavolo

# In[13]:

"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_table(dx, dy, dz):
    #: Larghezza della gamba del tevolo
    depth_leg = 0.05 * dx

    #: Distance della gamba dal bordo del tavolo
    distance_leg = 0.03 * dx

    depth_table = 0.05 * dz

    def makeLeg(dx, dy, dz):
        def baseChair(dx, dy, dz):
            first = PROD([
                PROD([
                    QUOTE([-distance_leg, dx - distance_leg * 2]),
                    QUOTE([-distance_leg, dy - distance_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])
            second = PROD([
                PROD([
                    QUOTE([-distance_leg - depth_leg, dx - distance_leg * 2 - depth_leg * 2]),
                    QUOTE([-distance_leg - depth_leg, dy - distance_leg * 2 - depth_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])

            return DIFF([
                first, second
            ])

        base_x = QUOTE([-distance_leg, depth_leg, - (dx - distance_leg * 2 - depth_leg * 2), depth_leg])
        base_y = QUOTE([-distance_leg, depth_leg, - (dy - distance_leg * 2 - depth_leg * 2), depth_leg])
        base_z = QUOTE([dz - depth_leg])

        return STRUCT([
            PROD([
                PROD([base_x, base_y]),
                base_z
            ]),
            baseChair(dx, dy, dz)
        ])

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT([
        makeLeg(dx, dy, dz - depth_table),
        T(3)(dz - depth_table),
        CUBOID([dx, dy, depth_table])
    ]))


# # Esempio

# In[14]:

v = ggpl_table(0.60, 1, 1)
print SIZE([1,2,3])(v)
VIEW(v)


# # Tavolo con sedia

# In[ ]:

"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_table_with_chair(dx, dy, dz):
    depth_leg = 0.05
    distance_leg = 0.03
    table = ggpl_table(dx, dy * 0.5, dz * 0.8, depth_leg, distance_leg)
    chair = ggpl_chair(dx - (depth_leg * 2 + distance_leg * 2 + 0.02), dy * 0.5, dz, depth_leg)

    return STRUCT([
        table,
        T([1,2])([depth_leg + distance_leg + 0.01, dy * 0.5]),
        chair
    ])


# ## Esempio

# In[ ]:

v = ggpl_table_with_chair(0.60, 1, 1)
print SIZE([1,2,3])(v)
VIEW(v)


# # Tavolo con sedia con braccioli

# In[ ]:

"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_table_with_chair_arm(dx, dy, dz):
    depth_leg = 0.05
    distance_leg = 0.03
    table = ggpl_table(dx, dy * 0.5, dz * 0.8, depth_leg, distance_leg)
    chair = ggpl_chair_with_arm(dx - (depth_leg * 2 + distance_leg * 2 + 0.02), dy * 0.5, dz, depth_leg)

    return STRUCT([
        table,
        T([1,2])([depth_leg + distance_leg + 0.01, dy * 0.5]),
        chair
    ])


# ## Esempio

# In[ ]:

v = ggpl_table_with_chair_arm(1, 1, 1)
print SIZE([1,2,3])(v)
VIEW(v)


# # Tavolo da mensa struttura base

# In[ ]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_table_canteen_base(dx, dy, dz):
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx
    depth_chair = 0.30 * dy

    def makeLeg(dx, dy, dz):
        return PROD([
            PROD([
                QUOTE([depth_leg, - (dx - depth_leg * 2), depth_leg]),
                QUOTE([depth_leg, - (dy - depth_leg * 2), depth_leg])
            ]),
            QUOTE([0, heigth_leg])
        ])

    def makeStruct(dx, dy, dz):
        return [
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([
                        depth_leg,
                        - dy + (depth_leg * 2),
                        depth_leg
                    ])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE([- (dx - depth_leg) / 2, depth_leg]),
                    QUOTE([-depth_leg, (dy - depth_leg * 2), -depth_leg])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE([- (dx - depth_leg) / 2 + depth_leg, depth_leg, - depth_leg, depth_leg]),
                    QUOTE([- depth_chair, depth_leg, - dy + depth_leg * 2 + depth_chair * 2, depth_leg])
                ]),
                QUOTE([-heigth_leg, dz - heigth_leg - depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([-depth_chair, dy - depth_chair * 2])
                ]),
                QUOTE([- dz + depth_table, depth_table])
            ])
        ]

    final = [makeLeg(dx,dy, dz)]
    final.extend(makeStruct(dx, dy, dz))

    return final


# # Tavolo da mensa con seduta unica

# In[ ]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_table_canteen(dx, dy, dz):
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx
    depth_chair = 0.30 * dy

    def makeChair(dx, dy, dz):
        return [
            PROD([
                PROD([
                    QUOTE([(dx - depth_leg) / 2, - depth_leg, (dx - depth_leg) / 2, 0]),
                    QUOTE([
                        - depth_chair + depth_leg,
                        depth_leg,
                        - dy + (depth_chair * 2),
                        depth_leg,
                    ])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([depth_chair, - dy + depth_chair * 2, depth_chair])
                ]),
                QUOTE([- depth_leg - heigth_leg, depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([depth_table, - dy + depth_table * 2, depth_table])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table, dz - depth_leg - heigth_leg - depth_table])
            ])
        ]

    final = ggpl_table_canteen_base(dx, dy, dz)
    final.extend(makeChair(dx, dy, dz))

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT(final))


# ## Esempio

# In[ ]:

v = ggpl_table_canteen(1, 1, 1)
print SIZE([1,2,3])(v)
VIEW(v)


# # Tavolo da mensa con seduta divisa

# In[ ]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_table_canteen_single_chair(dx, dy, dz):
    table = ggpl_table_canteen_base(dx, dy, dz)
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx
    depth_chair = 0.30 * dy

    def makeChair(dx, dy, dz):
        number_chair = math.floor(dx / depth_chair)

        if number_chair % 2 == 0:
            number_chair -= 1

        distance_chair = (dx / number_chair) - depth_chair
        distance_chair += distance_chair / (number_chair - 1)

        x = [depth_chair, -distance_chair] * (int(number_chair) - 1)
        x.append(depth_chair)

        return [
            PROD([
                PROD([
                    QUOTE([(dx - depth_leg) / 2, - depth_leg, (dx - depth_leg) / 2, 0]),
                    QUOTE([
                        - depth_chair + depth_leg ,
                        depth_leg,
                        - dy + (depth_chair * 2),
                        depth_leg,
                    ])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_chair, - dy + depth_chair * 2, depth_chair])
                ]),
                QUOTE([- depth_leg - heigth_leg, depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_table, - dy + depth_table * 2, depth_table])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table, dz - depth_leg - heigth_leg - depth_table])
            ])
        ]

    table.extend(makeChair(dx, dy, dz))

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT(table))


# ## Esempio

# In[ ]:

v = ggpl_table_canteen_single_chair(1, 1, 1)
print SIZE([1, 2, 3])(v)
VIEW(v)


# # Tavolo da mensa con sedute girevoli

# In[ ]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_table_canteen_turning_chair(dx, dy, dz):
    depth_chair = 0.30 * dy
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx

    def makeDisk():
        def disk2D(p):
            u, v = p
            return [v * COS(u), v * SIN(u)]

        domain2D = PROD([INTERVALS(2 * PI)(1280), INTERVALS(1)(3)])
        return STRUCT([
            T([1,2])([depth_chair / 1.825, depth_chair / 1.825]),
            S([1, 2])([depth_table / 2.0, depth_table / 2.0]),
            PROD([
                MAP(disk2D)(domain2D),
                QUOTE([- depth_leg - heigth_leg,depth_table])
            ])
        ])

    def makeChair(dx, dy, dz):
        number_chair = math.floor(dx / depth_chair)

        if number_chair % 2 == 0:
            number_chair -= 1

        distance_chair = (dx / number_chair) - depth_chair
        distance_chair += distance_chair / (number_chair - 1)

        x = [depth_chair, -distance_chair] * (int(number_chair) - 1)
        x.append(depth_chair)

        def makeGroupDisk():
            first = STRUCT([makeDisk(), T(1)(depth_chair + distance_chair)] * int(number_chair))

            final = [T(2)(dy - depth_chair - depth_leg)]
            final.extend([makeDisk(), T(1)(depth_chair + distance_chair)] * int(number_chair))

            return STRUCT([
                first,
                STRUCT(final)
            ])

        return [
            makeGroupDisk(),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_chair, - dy + depth_chair * 2, depth_chair])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table, depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_table, - dy + depth_table * 2, depth_table])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table * 2, dz - depth_leg - heigth_leg - depth_table])
            ])
        ]

    final = makeChair(dx, dy, dz)
    final.append(T(2)(depth_chair / 2.0))
    table = ggpl_table_canteen_base(dx, dy - depth_chair, dz)
    final.extend(table)

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT(final))


# ##  Esempio

# In[ ]:

v = ggpl_table_canteen_turning_chair(2, 2, 2)
print SIZE([1, 2, 3])(v)
VIEW(v)


# # Mobiletto - Struttura base

# In[24]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_mobile_base(dx, dy, dz):
    depth_chair = 0.03 * dy
    feet = 0.05 * dz
    distance_leg = 0.03 * dx
    depth_leg = 0.05 * dx

    def makeWall(dx, dy, dz):
        return [
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([0, dy])
                ]),
                QUOTE([depth_chair, - dz + depth_chair * 2, depth_chair, 0])
            ]),
            PROD([
                PROD([
                    QUOTE([depth_chair, - dx + depth_chair * 2, depth_chair, 0]),
                    QUOTE([0, dy])
                ]),
                QUOTE([-depth_chair, + dz - depth_chair * 2, -depth_chair, 0])
            ]),
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([- dy + depth_chair, depth_chair])
                ]),
                QUOTE([-depth_chair, + dz - depth_chair * 2, -depth_chair, 0])
            ])
        ]

    def makeFeet(dx, dy, dz):
        return [
            PROD([
                PROD([
                    QUOTE([-distance_leg, depth_leg, - dx + distance_leg * 2 + depth_leg * 2, depth_leg]),
                    QUOTE([-distance_leg, depth_leg, - dy + distance_leg * 2 + depth_leg * 2, depth_leg])
                ]),
                QUOTE([0, dz])
            ])
        ]

    final = makeFeet(dx, dy, feet)
    final.append(T(3)(feet))
    final.extend(makeWall(dx, dy, dz - feet))

    return STRUCT(final)


# # Cassetto per mobili

# In[25]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_mobile_drawer(dx, dy, dz):
    depth_chair = 0.03 * dy
    hole = 0.1 * dz
    return COLOR(intRGBColor([215, 190, 157]))(STRUCT([
        PROD([
            PROD([
                QUOTE([0, depth_chair, - dx + depth_chair * 2, depth_chair]),
                QUOTE([dy, 0])
            ]),
            QUOTE([0, dz])
        ]),
        PROD([
            PROD([
                QUOTE([0, dx]),
                QUOTE([- dy + depth_chair, depth_chair])
            ]),
            QUOTE([0, dz])
        ]),
        DIFF([
            PROD([
                PROD([
                    QUOTE([dx / 2.0, dx / 2.0]),
                    QUOTE([depth_chair / 2.0, depth_chair / 2.0])
                ]),
                QUOTE([dz / 2.0, dz / 2.0])
            ]),
            PROD([
                PROD([
                    QUOTE([- dx / 2.0 + hole / 2.0, hole]),
                    QUOTE([depth_chair / 2.0, depth_chair / 2.0])
                ]),
                QUOTE([-dz + hole, hole])
            ])
        ]),
        PROD([
            PROD([
                QUOTE([-depth_chair, dx - depth_chair * 2]),
                QUOTE([-depth_chair, dy - depth_chair])
            ]),
            QUOTE([0, depth_chair])
        ])
    ]))


# # Mobiletto con singolo cassetto

# In[16]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_mobile_single_drawer(dx, dy, dz):
    depth_chair = 0.03 * dy
    feet = 0.05 * dz
    mobile = ggpl_mobile_base(dx, dy, dz)

    final = [mobile]
    final.append(T([1,2,3])([depth_chair, 0, feet +depth_chair]))
    final.append(ggpl_mobile_drawer(dx - depth_chair * 2, dy -depth_chair, +dz - feet - depth_chair * 2))

    return STRUCT(final)


# ## Esempio

# In[17]:

v = ggpl_mobile_single_drawer(1, 1, 1)
print SIZE([1, 2, 3])(v)
VIEW(v)


# # Mobiletto con doppio cassetto

# In[18]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_mobile_double_drawer(dx, dy, dz):
    depth_chair = 0.03 * dy
    feet = 0.05 * dz
    mobile = ggpl_mobile_base(dx, dy, dz)

    final = [mobile]
    final.append(T([1,2,3])([depth_chair, 0, feet +depth_chair]))
    size = (+dz - feet - depth_chair * 2) / 2.0
    final.append(ggpl_mobile_drawer(dx - depth_chair * 2, dy -depth_chair, size))
    final.append(T(3)(size))
    final.append(ggpl_mobile_drawer(dx - depth_chair * 2, dy -depth_chair, size))

    return STRUCT(final)


# ## Esempio

# In[19]:

v = ggpl_mobile_double_drawer(1, 1, 1)
print SIZE([1, 2, 3])(v)
VIEW(v)


# # Mobiletto con n-cassetto

# In[22]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_mobile_drawer_n(dx, dy, dz, n = 3):
    depth_chair = 0.03 * dy
    feet = 0.05 * dz
    mobile = ggpl_mobile_base(dx, dy, dz)

    final = [mobile]
    final.append(T([1,2,3])([depth_chair, 0, feet +depth_chair]))
    size = (+dz - feet - depth_chair * 2) / float(n)

    final.extend([
        ggpl_mobile_drawer(dx - depth_chair * 2, dy - depth_chair, size),
        T(3)(size)
    ] * (n - 1))
    final.append(ggpl_mobile_drawer(dx - depth_chair * 2, dy -depth_chair, size))

    return STRUCT(final)


# ## Esempio 1

# In[26]:

v = ggpl_mobile_drawer_n(1, 1, 1)
print SIZE([1, 2, 3])(v)
VIEW(v)


# ## Esempio 2

# In[ ]:

v = ggpl_mobile_drawer_n(1, 1, 1, 5)
print SIZE([1, 2, 3])(v)
VIEW(v)


# ## Esempio 3

# In[ ]:

v = ggpl_mobile_drawer_n(1, 1, 1, 10)
print SIZE([1, 2, 3])(v)
VIEW(v)


# # Scrivania

# In[18]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_desk(dx, dy, dz):
    depth_leg = 0.05 * dx
    distance_leg = 0.03 * dx
    depth_table = 0.05 * dz

    table = ggpl_table(dx, dy, dz)

    def makePanel(dx, dy, dz):
        return [
            PROD([
                PROD([
                    QUOTE([-distance_leg,  depth_leg, - dx + distance_leg * 2 + depth_leg * 2, depth_leg]),
                    QUOTE([-distance_leg - depth_leg, dy - distance_leg * 2 - depth_leg * 2])
                ]),
                QUOTE([-depth_leg, dz - depth_leg * 4])
            ]),
            PROD([
                PROD([
                    QUOTE([-distance_leg - depth_leg, dx - distance_leg * 2 - depth_leg * 2]),
                    QUOTE([-dy + depth_leg + distance_leg, depth_leg])
                ]),
                QUOTE([-depth_leg, dz - depth_leg * 2 - depth_table])
            ])
        ]

    final = [table]
    final.extend(makePanel(dx, dy, dz))

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT(final))


# ## Esempio

# In[19]:

v = ggpl_desk(2, 1, 1)
print SIZE([1, 2, 3])(v)
VIEW(v)


# # Scrivania con cassettiera

# In[20]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_desk_mobile(dx, dy, dz, n = 3):
    depth_leg = 0.05 * dx
    distance_leg = 0.03 * dx
    depth_table = 0.05 * dz

    mobile = ggpl_mobile_drawer_n(dx * 0.25, dy - distance_leg - depth_leg, dz - depth_leg - depth_table - 0.1, n)
    desk = ggpl_desk(dx, dy, dz)

    return STRUCT([
        desk,
        T(1)(dx * 0.75 - distance_leg - depth_leg),
        mobile
    ])


# ## Esempio

# In[27]:

v = ggpl_desk_mobile(2, 1, 1)
print SIZE([1, 2, 3])(v)
VIEW(v)


# # Scrivania completta con cassettiera

# In[28]:


"""
:param dx: occupazione della struttura nelle x
:param dy: occupazione della struttura nelle y
:param dz: occupazione della struttura nelle z
"""
def ggpl_desk_mobile_chair(dx, dy, dz, n = 3):
    depth_leg = 0.05 * dx
    distance_leg = 0.03 * dx
    depth_table = 0.05 * dz

    mobile = ggpl_mobile_drawer_n(dx * 0.25, dy * 0.5 - distance_leg - depth_leg, dz - depth_leg - depth_table - 0.1, n)
    desk = ggpl_desk(dx, dy, dz)
    chair = STRUCT([
        R([1, 2])(math.pi),
        T([1, 2])([-dx * 0.25, -dy * 0.5]),
        ggpl_chair_with_arm(dx * 0.25, dy * 0.5, dz)
    ])

    return STRUCT([
        T(1)(dx *0.25),
        chair,
        T([1, 2])([-dx *0.25, dy * 0.5]),
        desk,
        T(1)(dx * 0.75 - distance_leg - depth_leg),
        mobile
    ])


# ## Esempio

# In[29]:

v = ggpl_desk_mobile_chair(2, 1, 1)
print SIZE([1, 2, 3])(v)
VIEW(v)


# In[ ]:



