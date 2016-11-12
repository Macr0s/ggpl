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


def ggpl_table_canteen_base(dx, dy, dz):
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx
    depth_chair = 0.30 * dy

    def makeLeg(dx, dy, dz):
        return PROD([
            PROD([
                QUOTE([depth_leg, - (dx - depth_leg * 2), depth_leg]),
                QUOTE([depth_leg, - (dy - depth_leg * 2), depth_leg])
            ]),
            QUOTE([0, heigth_leg])
        ])

    def makeStruct(dx, dy, dz):

        return [
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([
                        depth_leg,
                        - dy + (depth_leg * 2),
                        depth_leg
                    ])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE([- (dx - depth_leg) / 2, depth_leg]),
                    QUOTE([-depth_leg, (dy - depth_leg * 2), -depth_leg])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE([- (dx - depth_leg) / 2 + depth_leg, depth_leg, - depth_leg, depth_leg]),
                    QUOTE([- depth_chair, depth_leg, - dy + depth_leg * 2 + depth_chair * 2, depth_leg])
                ]),
                QUOTE([-heigth_leg, dz - heigth_leg - depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([-depth_chair, dy - depth_chair * 2])
                ]),
                QUOTE([- dz + depth_table, depth_table])
            ])
        ]

    final = [makeLeg(dx,dy, dz)]
    final.extend(makeStruct(dx, dy, dz))

    return final


def ggpl_table_canteen(dx, dy, dz):
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx
    depth_chair = 0.30 * dy

    def makeChair(dx, dy, dz):
        return [
            PROD([
                PROD([
                    QUOTE([(dx - depth_leg) / 2, - depth_leg, (dx - depth_leg) / 2, 0]),
                    QUOTE([
                        - depth_chair + depth_leg,
                        depth_leg,
                        - dy + (depth_chair * 2),
                        depth_leg,
                    ])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([depth_chair, - dy + depth_chair * 2, depth_chair])
                ]),
                QUOTE([- depth_leg - heigth_leg, depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE([0, dx]),
                    QUOTE([depth_table, - dy + depth_table * 2, depth_table])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table, dz - depth_leg - heigth_leg - depth_table])
            ])
        ]

    final = ggpl_table_canteen_base(dx, dy, dz)
    final.extend(makeChair(dx, dy, dz))

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT(final))


def ggpl_table_canteen_single_chair(dx, dy, dz):
    table = ggpl_table_canteen_base(dx, dy, dz)
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx
    depth_chair = 0.30 * dy

    def makeChair(dx, dy, dz):
        number_chair = math.floor(dx / depth_chair)

        if number_chair % 2 == 0:
            number_chair -= 1

        distance_chair = (dx / number_chair) - depth_chair
        distance_chair += distance_chair / (number_chair - 1)

        x = [depth_chair, -distance_chair] * (int(number_chair) - 1)

        x.append(depth_chair)

        return [
            PROD([
                PROD([
                    QUOTE([(dx - depth_leg) / 2, - depth_leg, (dx - depth_leg) / 2, 0]),
                    QUOTE([
                        - depth_chair + depth_leg ,
                        depth_leg,
                        - dy + (depth_chair * 2),
                        depth_leg,
                    ])
                ]),
                QUOTE([-heigth_leg, depth_leg])
            ]),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_chair, - dy + depth_chair * 2, depth_chair])
                ]),
                QUOTE([- depth_leg - heigth_leg, depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_table, - dy + depth_table * 2, depth_table])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table, dz - depth_leg - heigth_leg - depth_table])
            ])
        ]

    table.extend(makeChair(dx, dy, dz))

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT(table))


def ggpl_table_canteen_turning_chair(dx, dy, dz):
    depth_chair = 0.30 * dy
    depth_leg = 0.030 * dx
    heigth_leg = 0.45 * dz - depth_leg
    depth_table = 0.03 * dx

    def makeDisk():
        def disk2D(p):
            u, v = p
            return [v * COS(u), v * SIN(u)]

        domain2D = PROD([INTERVALS(2 * PI)(32), INTERVALS(1)(3)])
        return STRUCT([
            T([1,2])([depth_chair / 1.825, depth_chair / 1.825]),
            S([1, 2])([depth_table / 2.0, depth_table / 2.0]),
            PROD([
                MAP(disk2D)(domain2D),
                QUOTE([- depth_leg - heigth_leg,depth_table])
            ])
        ])

    def makeChair(dx, dy, dz):
        number_chair = math.floor(dx / depth_chair)

        if number_chair % 2 == 0:
            number_chair -= 1

        distance_chair = (dx / number_chair) - depth_chair
        distance_chair += distance_chair / (number_chair - 1)

        x = [depth_chair, -distance_chair] * (int(number_chair) - 1)
        x.append(depth_chair)

        def makeGroupDisk():
            first = STRUCT([makeDisk(), T(1)(depth_chair + distance_chair)] * int(number_chair))

            final = [T(2)(dy - depth_chair - depth_leg)]
            final.extend([makeDisk(), T(1)(depth_chair + distance_chair)] * int(number_chair))

            return STRUCT([
                first,
                STRUCT(final)
            ])

        return [
            makeGroupDisk(),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_chair, - dy + depth_chair * 2, depth_chair])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table, depth_table])
            ]),
            PROD([
                PROD([
                    QUOTE(x),
                    QUOTE([depth_table, - dy + depth_table * 2, depth_table])
                ]),
                QUOTE([- depth_leg - heigth_leg - depth_table * 2, dz - depth_leg - heigth_leg - depth_table])
            ])
        ]

    final = makeChair(dx, dy, dz)
    final.append(T(2)(depth_chair / 2.0))
    table = ggpl_table_canteen_base(dx, dy - depth_chair, dz)
    final.extend(table)

    return COLOR(intRGBColor([215, 190, 157]))(STRUCT(final))

v = ggpl_table_canteen_turning_chair(2, 2, 2)
print SIZE([1, 2, 3])(v)
VIEW(v)