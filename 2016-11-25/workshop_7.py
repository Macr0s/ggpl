from pyplasm import *



def intRGBColor(values):
    """ intRGBColor

    Metodo preso dal web per ottenere colori da RGB
    :param values: lista di tre interi RGB
    :return: Color4f
    """
    return Color4f([
        values[0]/255.0,
        values[1]/255.0,
        values[2]/255.0,
        1
    ])

GOLD = intRGBColor([238,232,170])
#: Colore oro

LIGHT_BLUE = intRGBColor([192,242,247])
#: Colore blue chiaro

LIGHT_BROWN = intRGBColor([193,157,98])
#: Colore Legno


def ggpl_simply_window_door(x, y, z, occupacy):
    """ ggpl_simply_window_door

    Metodo che crea la struttura base della finestra e della porta

    :param x: proiezione della finestra sulla x
    :param y: proiezione della finestra sulla y
    :param z: proiezione della finestra sulla z
    :param occupacy: matrice che presenta le zone dove ci sta il vetro o il legno
    :return: hpc della struttura base della porta e della finestra
    """

    offset = 0
    #: Posizione parziale sulla y di ogni parte della struttura

    glass_depth = 0.2
    #: Spessore del vestro

    final = []
    #: Lista dove sono contenuti tutti gli hpc parziali

    def generate(t):
        """ generate

        Metodo che serve per generare il legno o uno spazio vuoto

        :param t: grandezza della parte
        :return:  un float positivo per il legno e uno negativo per il legno
        """
        return t[0] * (1 if t[1] == 1 else -1)

    def generate_glass(t):
        """ generate_glass

        Metodo che serve per generare il vetro o uno spazio vuoto

        :param t: grandezza della parte
        :return:  un float positivo per il legno e uno negativo per il vetro
        """
        return t[0] * (-1 if t[1] == 1 else 1)

    def foundNegative(list):
        """ foundNegative

        Metodo per determinare se e' presente uno spazio vuoto nella lista passata come parametro

        :param list: una lista
        :return: un booleano
        """
        for i in range(len(list)):
            if list[i] > 0:
                return False
        return True

    for i in range(len(occupacy)):
        final.append(COLOR(LIGHT_BROWN)(PROD([
            PROD([
                QUOTE(map(generate, zip(x, occupacy[i]))),
                QUOTE([-offset, y[i]])
            ]),
            QUOTE([z[0] / 2.0, z[0] / 2.0])
        ])))

        colum = map(generate_glass, zip(x, occupacy[i]))

        if not foundNegative(colum):
            final.append(COLOR(LIGHT_BLUE)(PROD([
                PROD([
                    QUOTE(colum),
                    QUOTE([-offset, y[i]])
                ]),
                QUOTE([-z[0] / 2.0 + glass_depth / 2.0, glass_depth])
            ])))

        offset += y[i]

    return STRUCT(final)


def sumPartial(list, max):
    """ sumPartial

    Metodo che calcola la somma parziale fino ad un indice

    :param list: una lista
    :param max: l'indice
    :return: il valore della somma paziale
    """
    height = 0.0
    for i in range(max):
        height += list[i]

    return height


def ggpl_window(x, y, z, occupacy):
    """
    Metodo che crea la struttura della finestra

    :param x: proiezione della finestra sulla x
    :param y: proiezione della finestra sulla y
    :param z: proiezione della finestra sulla z
    :param occupacy: matrice che presenta le zone dove ci sta il vetro o il legno
    :return: hpc della struttura della finestra
    """
    def makeKnob():
        """ makeKnob

        Metodo che crea il pomello

        :return: una lista di hpc che rappresenta il pomello
        """

        depth_knob = [3,4,0.2]
        #: Dimensione del pmello

        def allPositive(list):
            for i in range(len(list)):
                if list[i] == 0:
                    return False
            return True

        first = 0
        #: Variabile intera per dire se va messo oppure no il pomello. Se vale 1 allora va messo


        for i in range(len(occupacy)):
            check = allPositive(occupacy[i])
            #: Condizione base per creare il pomello

            if check and first == 1:
                offest = z[0]
                #: Grandezza della finestra

                size = SUM(x)
                #: Larghezza della finestra

                space = y[i]
                #: Grandezza massima del pomello

                height = sumPartial(y, i)
                #: Posizione del pomello sulle y rispetto all'origine

                return [
                    COLOR(GOLD)(PROD([
                        PROD([
                            QUOTE([- size / 2.0 + depth_knob[0] / 2.0, depth_knob[0]]),
                            QUOTE([- height, space])
                        ]),
                        QUOTE([-offest, depth_knob[2]])
                    ])),
                    COLOR(GOLD)(PROD([
                        PROD([
                            QUOTE([- size / 2.0 + depth_knob[0] / 2.0, depth_knob[0]]),
                            QUOTE([- height - space / 2.0, space / 2.0])
                        ]),
                        QUOTE([-offest -depth_knob[2], depth_knob[2]])
                    ]))
                ]
            elif check and first == 0:
                first = 1

    def scale(dx, dy, dz):
        """ scale

        Metodo per scalare la finestra

        :param dx: Il fattore di scala sulle x
        :param dy: Il fattore di scala sulle y
        :param dz: Il fattore di scala sulle z
        :return: La finestra scalata
        """

        final = [
            S([1, 2, 3])([dx, dy, dz]),
            ggpl_simply_window_door(x, y, z, occupacy),
        ]

        final.extend(makeKnob())

        return STRUCT(final)

    return scale


X=[1,5,1,5,1,5,1,5,1]
Y=[1,10,1,10,1,10,1]
Z=[1]
occupacy=[
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1]]

window = ggpl_window(X,Y,Z,occupacy)(1,1,1)

print(SIZE([1,2,3])(window))

VIEW(window)


def ggpl_door(x, y, z, occupacy):
    """
    Metodo che crea la struttura della porta

    :param x: proiezione della porta sulla x
    :param y: proiezione della porta sulla y
    :param z: proiezione della porta sulla z
    :param occupacy: matrice che presenta le zone dove ci sta il vetro o il legno
    :return: hpc della struttura della porta
    """

    def makeKnob(size):
        """ makeKnob

        Metodo che crea il pomello

        :param size: La grandezza della finestra sulla x
        :return: una lista di hpc che rappresenta il pomello
        """

        space = y[4]
        #: Grandezza della zona dove puo' essere messo il pomello

        height = sumPartial(y, 5)
        #: Altezza massima del pomello rispetto l'asse x

        depth_knob = 1
        #: Grandezza del pomello
        return [
            COLOR(GOLD)(PROD([
                PROD([
                    QUOTE([- size / 2.0 + depth_knob, depth_knob]),
                    QUOTE([- height + space / 2.0, depth_knob])
                ]),
                QUOTE([-z[0], depth_knob])
            ]))
        ]


    def scale(dx, dy, dz):
        """ scale

        Metodo per scalare la porta

        :param dx: Il fattore di scala sulle x
        :param dy: Il fattore di scala sulle y
        :param dz: Il fattore di scala sulle z
        :return: La porta scalata
        """

        structure = ggpl_simply_window_door(x, y, z, occupacy)
        #: Struttura base della finestra

        size = SIZE([1, 2, 3])(structure)
        #: Occupazione della finestra nell'asse x, y, z

        final = [
            S([1, 2, 3])([dx, dy, dz]),
            structure
        ]

        final.extend(makeKnob(size[0]))

        return STRUCT(final)

    return scale

X = [2, 3, 1, 3, 2, 2, 3, 1, 3, 1, 3, 2, 2, 3, 1, 3, 1, 3, 2, 2, 3, 1, 3, 2]
Y = [5, 5, 2, 1, 5, 1, 5, 1, 5, 1, 5, 1, 2, 1]
Z = [1]
occupacy=[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

VIEW(ggpl_door(X,Y,Z, occupacy)(1, 1, 1))