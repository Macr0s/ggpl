from pyplasm import *


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

    def intRGBColor(values):
        return Color4f([values[0] / 255.0,
                        values[1] / 255.0,
                        values[2] / 255.0,
                        1.0])

    return STRUCT([
        COLOR(BLACK)(makeLeg(dx, dy, height_leg)),
        T(3)(height_leg),
        COLOR(intRGBColor([215, 190, 157]))(CUBOID([dx, dy, depth_chair])),
        T(2)(dy - depth_chair),
        COLOR(intRGBColor([215, 190, 157]))(CUBOID([dx, depth_chair, dz - depth_chair - height_leg]))
    ])


def ggpl_chair_with_arm(dx, dy, dz, depth_leg=0.015, distance_leg=0.03, depth_chair=0.01, height_leg=0.45):
    chair = ggpl_chair(dx, dy, dz, depth_leg, distance_leg, depth_chair, height_leg)



def ggpl_desk_with_chair(dx, dy, dz):

    return ggpl_chair_with_arm(dx, dy, dz)

VIEW(ggpl_desk_with_chair(0.40, 0.40, 0.9))