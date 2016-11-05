from pyplasm import *


def ggpl_hip_roof(verts, cells):
    roof = []

    def makeRidge(verts, cells):
        remove=[]

        def findFN(x):
            if not x[2] == 0:
                remove.append(x)
            return x

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

    def makeStructure(verts, cells):
        return OFFSET([0.1, 0.2, 0.1])(SKEL_1(MKPOL([verts,cells,None])))

    ridge = makeRidge(verts, cells)
    struct = makeStructure(verts, cells)

    roof.append(COLOR(RED)(ridge))
    roof.append(struct)
    return STRUCT(roof)

def ggpl_hip_roof_hpc(roof):
    def cleanUKPOL(skel):
        points, cells, none = UKPOL(skel)

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

        def searchFN(x):
            def replace (y):
                for i in range(len(support)):
                    if support[i][1] == y:
                        return support[i][0]
                return y

            return map(replace, x)

        cells_new = map(searchFN, cells)

        return [points, cells_new]

    verts, cells = cleanUKPOL(roof)

    roof = []

    def makeRidge(verts, cells):
        remove = []

        def findFN(x):
            if not x[2] == 0:
                remove.append(x)
            return x

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

    def makeStructure(verts, cells):
        return OFFSET([0.1, 0.2, 0.1])(SKEL_1(MKPOL([verts, cells, None])))

    ridge = makeRidge(verts, cells)
    struct = makeStructure(verts, cells)

    roof.append(COLOR(RED)(ridge))
    roof.append(struct)
    return STRUCT(roof)

VIEW(ggpl_hip_roof([
    [0,0,0],[0,10,0],[5,5,0],[5,5,5],[15,0,0],[15,10,0],[10,5,0],[10,5,5]
],
[
    [3,4,2,1],[8,5,6,7],[5,8,7,3,4,1],[2,4,3,7,8,6]
]))

VIEW(ggpl_hip_roof([
    [0, 0, 0], [10, 0, 0], [8, 2, 4], [2, 2, 4], [2, 2, 0], [8, 2, 0],
    [8, 2, 0], [2, 2, 0], [2, 2, 4], [8, 2, 4], [10, 4, 0], [4, 4, 0],
    [10, 0, 0], [10, 4, 0], [8, 2, 0], [8, 2, 4],
    [0, 0, 0], [0, 10, 0], [2, 8, 0], [2, 2, 0], [2, 2, 4], [2, 8, 4],
    [2, 2, 0], [4, 4, 0], [4, 10, 0], [2, 8, 0], [2, 2, 4], [2, 8, 4],
    [0, 10, 0], [4, 10, 0], [2, 8, 0], [2, 8, 4]
],[
    [1, 2, 3, 4, 5, 6],
    [7, 8, 9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22],
    [23, 24, 25, 26, 27, 28],
    [29, 30, 31, 32]
]))

VIEW(ggpl_hip_roof_hpc(MKPOL([
    [
        [0,0,0],[0,10,0],[5,5,0],[5,5,5],[15,0,0],[15,10,0],[10,5,0],[10,5,5]
    ],
    [
        [3,4,2,1],[8,5,6,7],[5,8,7,3,4,1],[2,4,3,7,8,6]
    ],
    None
])))
