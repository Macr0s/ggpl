from pyplasm import *


def ggpl_windows(x, y, z, occupacy):
    offset = 0
    glass_depth = 0.2
    final = []

    def generate(t):
        return t[0] * (1 if t[1] == 1 else -1)

    def generate_glass(t):
        return t[0] * (-1 if t[1] == 1 else 1)

    def allNegative(list):
        for i in range(len(list)):
            if list[i] > 0:
                return False
        return True

    for i in range(len(occupacy)):
        final.append(COLOR(BROWN)(PROD([
            PROD([
                QUOTE(map(generate, zip(x, occupacy[i]))),
                QUOTE([-offset, y[i]])
            ]),
            QUOTE([z[0] / 2.0, z[0] / 2.0])
        ])))

        colum = map(generate_glass, zip(x,  occupacy[i]))

        if not allNegative(colum):
            final.append(COLOR(WHITE)(PROD([
                    PROD([
                        QUOTE(colum),
                    QUOTE([-offset, y[i]])
                ]),
                QUOTE([-z[0] / 2.0 + glass_depth / 2.0, glass_depth])
            ])))

        offset += y[i]

    def scale(dx, dy, dz):

        return STRUCT([
            S([1, 2, 3])([dx, dy, dz]),
            STRUCT(final)

        ])

    return scale


X=[1,5,1,5,1,5,1,5,1]
Y=[1,10,1,10,1,10,1]
Z=[1]
mirror_or_not_mirror=[
    [1,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1]]

window = ggpl_windows(X,Y,Z,mirror_or_not_mirror)(1,1,1)

print(SIZE([1,2,3])(window))

VIEW(window)

window = ggpl_windows(X,Y,Z,mirror_or_not_mirror)(2,2,2)

print(SIZE([1,2,3])(window))

VIEW(window)