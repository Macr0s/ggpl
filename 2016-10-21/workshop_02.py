from pyplasm import *
import csv

"""http://www.calcolostrutture.com/public/uploaded/News_911_01.jpg"""

def ggpl_bone_structure(file_name):
    def planeStructure(beamSection, pillarSection, distancePillars, intersectHeights):
        fStructs = []

        def createFinalStruct(startPoint, height):
            pillar = CUBOID([pillarSection[0], pillarSection[1], height])
            return STRUCT([T(2)(startPoint), pillar])

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

    def createBaseFrame(origin, beamSection, pillarSection, distancePillars, intersectHeights):
        return STRUCT([
            T([1,2,3])([origin[0], origin[1], origin[2]]),
            planeStructure(beamSection, pillarSection, distancePillars, intersectHeights)
        ])

    def createTrasversalBean():
        return 0

    frames = []
    odd = True
    origin = [0, 0, 0]
    with open(file_name, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if odd :
                odd = False
                origin = [origin[0] + float(row[0]), origin[1] + float(row[1]), origin[2] + float(row[2])]
            else:
                odd = True
                beamSection = [float(row[0]), float(row[1])]
                pillarSection = [float(row[2]), float(row[3])]

                distancePillars = []
                start_point =  5
                finish_point = int(row[4]) + start_point
                for index in range(start_point, finish_point):
                    distancePillars.append(int(row[index]))

                intersectHeights = []
                start_point = finish_point + 1
                finish_point = int(row[finish_point]) + start_point
                for index in range(start_point, finish_point):
                    intersectHeights.append(int(row[index]))

                frames.append(createBaseFrame(origin, beamSection, pillarSection, distancePillars, intersectHeights))
    return STRUCT(frames)


VIEW(ggpl_bone_structure("frame_data_457024.csv"))