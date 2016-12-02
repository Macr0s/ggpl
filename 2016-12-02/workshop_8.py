from pyplasm import *
import csv


def createStructFromLines(file_name, size, color):
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

    return COLOR(color)(
        OFFSET([size, size])(
            MKPOL([
                points,
                indexs,
                None
            ])
        )
    )


if __name__ == "__main__":
    externalWall = createStructFromLines("pianimetria/lines/Muro Esterno.lines", 4, RED)
    internalWall = createStructFromLines("pianimetria/lines/Strutture interne.lines", 4, GREEN)
    windows = createStructFromLines("pianimetria/lines/Finestre.lines", 4, BLACK)
    doors = createStructFromLines("pianimetria/lines/Porte.lines", 4, WHITE)
    pillars = createStructFromLines("pianimetria/lines/Colonne Interne.lines", 4, MAGENTA)
    balconies = createStructFromLines("pianimetria/lines/Terrazzi.lines", 4, ORANGE)

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
        PROD([
            external,
            QUOTE([100])
        ]),
        PROD([
            internal,
            QUOTE([100])
        ]),
    ]))

