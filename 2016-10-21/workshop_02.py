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

    def lookahead(iterable):
        """Pass through all values from the given iterable, augmented by the
        information if there are more values to come after the current one
        (True), or if it is the last value (False).
        """
        # Get an iterator and pull the first value.
        it = iter(iterable)
        last = next(it)
        # Run the iterator to exhaustion (starting from the second value).
        for val in it:
            # Report the *previous* value (more to come).
            yield last, True
            last = val
        # Report the last value.
        yield last, False

    def createTrasversalBeam(distance, beamSection, pillarSection, distancePillars, intersectHeights):
        y = []
        for index in range(len(distancePillars)):
            y.append(pillarSection[1])
            y.append(- distancePillars[index])
        y.append(pillarSection[1])

        x = [
            - pillarSection[0],
            distance
        ]

        z = []
        for i in range(len(intersectHeights)):
            if i == 0:
                z.append(-intersectHeights[i])
            else:
                z.append(-intersectHeights[i] + beamSection[1])
            z.append(beamSection[1])

        return PROD([
                PROD([QUOTE(x), QUOTE(y)]),
                QUOTE(z)
        ])

    frames = []
    odd = True
    distance = 0
    transaction = None
    with open(file_name, 'rb') as csvfile:
        builderreader = csv.reader(csvfile)

        for row, has_more in lookahead(builderreader):
            if odd :
                odd = False
                distance = float(row[0])
                transaction = T([1,2,3])([float(row[0]), float(row[1]), float(row[2])])
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

                frames.append(
                    planeStructure(beamSection, pillarSection, distancePillars, intersectHeights)
                )

                if has_more:
                    frames.append(
                        createTrasversalBeam(
                            distance,
                            beamSection,
                            pillarSection,
                            distancePillars,
                            intersectHeights
                        )
                    )

                frames.append(transaction)

    return STRUCT(frames)


VIEW(ggpl_bone_structure("simple_frame_data_457024.csv"))