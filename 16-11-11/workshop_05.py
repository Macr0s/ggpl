from pyplasm import *


def intRGBColor(values):
    return Color4f([values[0] / 255.0,
                    values[1] / 255.0,
                    values[2] / 255.0,
                    1.0])


def ggpl_chair(dx, dy, dz, depth_leg=0.015, distance_leg=0.03, depth_chair=0.01, height_leg=0.45):
    def makeLeg(dx, dy, dz):
        def baseChair(dx, dy, dz):
            first = PROD([
                PROD([
                    QUOTE([-distance_leg, dx - distance_leg * 2]),
                    QUOTE([-distance_leg, dy - distance_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])
            second = PROD([
                PROD([
                    QUOTE([-distance_leg - depth_leg, dx - distance_leg * 2 - depth_leg * 2]),
                    QUOTE([-distance_leg - depth_leg, dy - distance_leg * 2 - depth_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])

            return DIFF([
                first, second
            ])

        base_x = QUOTE([-distance_leg, depth_leg, - (dx - distance_leg * 2 - depth_leg * 2), depth_leg])
        base_y = QUOTE([-distance_leg, depth_leg, - (dy - distance_leg * 2 - depth_leg * 2), depth_leg])
        base_z = QUOTE([dz - depth_leg])

        return STRUCT([
            PROD([
                PROD([base_x, base_y]),
                base_z
            ]),
            baseChair(dx, dy, dz)
        ])

    return STRUCT([
        COLOR(BLACK)(makeLeg(dx, dy, height_leg)),
        T(3)(height_leg),
        COLOR(intRGBColor([215, 190, 157]))(CUBOID([dx, dy, depth_chair])),
        T(2)(dy - depth_chair),
        COLOR(intRGBColor([215, 190, 157]))(CUBOID([dx, depth_chair, dz - depth_chair - height_leg]))
    ])


def ggpl_chair_with_arm(dx, dy, dz, depth_leg=0.015, distance_leg=0.03, depth_chair=0.01, height_leg=0.45):
    chair = ggpl_chair(dx - depth_leg * 4, dy, dz, depth_leg, distance_leg, depth_chair, height_leg)

    def makeArm(dx, dy, dz, right=True):
        def supportArm():
            return COLOR(BLACK)(STRUCT([
                T([2,3])([distance_leg,height_leg - depth_leg]),
                CUBOID([depth_leg * 2 + distance_leg, depth_leg, depth_leg]),
                T([2])([dy - distance_leg * 2 - depth_leg]),
                CUBOID([depth_leg * 2 + distance_leg, depth_leg, depth_leg])
            ]))

        base = [
            COLOR(BLACK)(PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([-distance_leg, depth_leg, - (dy - distance_leg * 2 - depth_leg * 2), depth_leg])
                ]),
                QUOTE([-height_leg, (dz - height_leg - depth_leg) * 0.5])
            ])),
            COLOR(intRGBColor([215, 190, 157]))(PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([-distance_leg, dy - distance_leg * 2])
                ]),
                QUOTE([- (height_leg + (dz - height_leg - depth_leg) * 0.5), depth_leg])
            ]))
        ]

        final = [supportArm()]

        if not right:
            final = [
                supportArm(),
                T(1)(distance_leg + depth_leg)
            ]

        final.extend(base)

        return STRUCT(final)

    return STRUCT([
        makeArm(depth_leg, dy, dz),
        T(1)(depth_leg*2),
        chair,
        T(1)(dx - depth_leg * 4 - distance_leg),
        makeArm(depth_leg, dy, dz, False)
    ])


def ggpl_chair_with_desk(dx, dy, dz, depth_leg=0.015, distance_leg=0.03, depth_chair=0.01, height_leg=0.45):
    chair = ggpl_chair_with_arm(dx, dy * 0.7, dz, depth_leg, distance_leg, depth_chair, height_leg)

    def makeDesk(dx, dy, dz):
        return STRUCT([
            COLOR(intRGBColor([215, 190, 157]))(PROD([
                PROD([
                    QUOTE([dx, 0]),
                    QUOTE([dy, 0])
                ]),
                QUOTE([- (height_leg + (dz - height_leg - depth_leg) * 0.5), depth_leg])
            ])),
            T([2, 3])([dy, height_leg + (dz - height_leg - depth_leg) * 0.5]),
            COLOR(BLACK)(CUBOID([depth_leg, distance_leg, depth_leg]))
        ])

    return STRUCT([
        makeDesk(dx * 0.75, dy * 0.3, dz),
        T(2)(dy * 0.3),
        chair
    ])


def ggpl_table(dx, dy, dz, depth_leg=0.05, distance_leg=0.03, depth_table=0.05):
    def makeLeg(dx, dy, dz):
        def baseChair(dx, dy, dz):
            first = PROD([
                PROD([
                    QUOTE([-distance_leg, dx - distance_leg * 2]),
                    QUOTE([-distance_leg, dy - distance_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])
            second = PROD([
                PROD([
                    QUOTE([-distance_leg - depth_leg, dx - distance_leg * 2 - depth_leg * 2]),
                    QUOTE([-distance_leg - depth_leg, dy - distance_leg * 2 - depth_leg * 2])
                ]),
                QUOTE([- dz + depth_leg, depth_leg])
            ])

            return DIFF([
                first, second
            ])

        base_x = QUOTE([-distance_leg, depth_leg, - (dx - distance_leg * 2 - depth_leg * 2), depth_leg])
        base_y = QUOTE([-distance_leg, depth_leg, - (dy - distance_leg * 2 - depth_leg * 2), depth_leg])
        base_z = QUOTE([dz - depth_leg])

        return STRUCT([
            PROD([
                PROD([base_x, base_y]),
                base_z
            ]),
            baseChair(dx, dy, dz)
        ])

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT([
        makeLeg(dx, dy, dz - depth_table),
        T(3)(dz - depth_table),
        CUBOID([dx, dy, depth_table])
    ]))


def ggpl_table_with_chair(dx, dy, dz):
    depth_leg = 0.05
    distance_leg = 0.03
    table = ggpl_table(dx, dy * 0.5, dz * 0.8, depth_leg, distance_leg)
    chair = ggpl_chair(dx - (depth_leg * 2 + distance_leg * 2 + 0.02), dy * 0.5, dz, depth_leg)

    return STRUCT([
        table,
        T([1,2])([depth_leg + distance_leg + 0.01, dy * 0.5]),
        chair
    ])


def ggpl_table_with_chair_arm(dx, dy, dz):
    depth_leg = 0.05
    distance_leg = 0.03
    table = ggpl_table(dx, dy * 0.5, dz * 0.8, depth_leg, distance_leg)
    chair = ggpl_chair_with_arm(dx - (depth_leg * 2 + distance_leg * 2 + 0.02), dy * 0.5, dz, depth_leg)

    return STRUCT([
        table,
        T([1,2])([depth_leg + distance_leg + 0.01, dy * 0.5]),
        chair
    ])


"""def ggpl_table_canteen(dx, dy, dz):"""



v = ggpl_table_with_chair_arm(0.60, 1, 1)
print SIZE([1,2,3])(v)
VIEW(v)