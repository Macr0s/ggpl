from pyplasm import *
import csv


def createStructFromLines(file_name):
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

    return MKPOL([
        points,
        indexs,
        None
    ])


if __name__ == "__main__":
    externalWall = createStructFromLines("pianimetria/lines/Muro Esterno.lines")
    internalWall = createStructFromLines("pianimetria/lines/Strutture interne.lines")
    windows = createStructFromLines("pianimetria/lines/Finestre.lines")
    doors = createStructFromLines("pianimetria/lines/Porte.lines")
    pillars = createStructFromLines("pianimetria/lines/Colonne Interne.lines")
    balconies = createStructFromLines("pianimetria/lines/Terrazzi.lines")

