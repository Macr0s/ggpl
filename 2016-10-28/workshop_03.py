from pyplasm import *
from math import *


def ggpl_l_shaped_stair(dx, dy, dz):
    def makeStep(tread, riser):
        base = MKPOL([[[0, 0], [0, riser], [tread, riser], [2 * tread, riser], [tread, 0]], [[1, 2, 3, 4, 5]], 1])
        base = PROD([base, QUOTE([1])])

        return STRUCT([
            R([1, 3])(-math.pi / 2),
            R([1, 2])(-3 * math.pi / 2),
            base
        ])

    def stairValue(dz):
        step = math.floor(dz * 100 / 18) + 1
        riser = dz * 100 / step
        tread = 64 - 2 * riser

        return [int(step), riser / 100, tread / 100]

    def makeStair(step, riser, tread):
        steps = []
        for i in range(step):
            if i != 0:
                steps.append(T([2, 3])([tread, riser]))
            steps.append(makeStep(tread, riser))

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

            stairs.append(CUBOID([1, 1, riser]))
            stairs.append(T(2 if stay_on_x else 1)(1))
            stairs.append(T(1 if stay_on_x else 2)(1))
            stairs.append(R([1, 2])(- math.pi / 2.0))
            stairs.append(T(3)(riser))

            stay_on_x = not stay_on_x
            way += + 1 if way != 2 else 0

    return STRUCT(stairs)

stair = ggpl_l_shaped_stair(4,3,10)
print SIZE([1,2,3])(stair)

VIEW(stair)
