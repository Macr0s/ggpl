from pyplasm import *
import csv


def createStructFromLines(file_name, size):
    points = []
    indexs = []
    i = 0

    with open(file_name, 'rb') as csvfile:
        builderreader = csv.reader(csvfile)

        for row in builderreader:
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


if __name__ == "__main__":
    externalWall = createStructFromLines("pianimetria/lines/Muro Esterno.lines", 4)
    internalWall = createStructFromLines("pianimetria/lines/Strutture interne.lines", 4)
    windows = createStructFromLines("pianimetria/lines/Finestre.lines", 6)
    doors = createStructFromLines("pianimetria/lines/Porte.lines", 6)
    pillars = createStructFromLines("pianimetria/lines/Colonne Interne.lines", 4)
    balconies = createStructFromLines("pianimetria/lines/Terrazzi.lines", 4)
    internalFloor = createFloorFromLines("pianimetria/lines/Muro Esterno.lines", 4)

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
        internalFloor
    ]))

