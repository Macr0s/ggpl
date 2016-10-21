from pyplasm import *

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
            if iterator != len(distancePillars) - 1:
                fStructs.append(createFStruct(startDistance, height, distancePillars[iterator]))
            else:
                fStructs.append(createFinalStruct(startDistance, height))

            startDistance = startDistance + pillarSection[1] + distancePillars[iterator]

        return STRUCT(fStructs)



VIEW(ggpl_bone_structure("frame_data_457024.csv"))