from .elements.CubeElements import FaceDirection


def f2l_1(cube, next_face):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)


def f2l_2(cube, current):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)


def f2l_3(cube, current):
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)


def f2l_4(cube, next_face):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_5(cube, next_face):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)


def f2l_6(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_7(cube, next_face):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)


def f2l_8(cube, current):
    for _ in range(2):
        cube.make_rotation(FaceDirection.UP, True)
        cube.make_rotation(current, False)
        cube.make_rotation(FaceDirection.UP, True)
        cube.make_rotation(FaceDirection.UP, True)
        cube.make_rotation(current, True)


def f2l_9(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)


def f2l_10(cube, next_face):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_11(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)


def f2l_12(cube, next_face):
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)


def f2l_13(cube, current):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)


def f2l_14(cube, next_face):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_15(cube, next_face, prev_face, back_face):
    cube.make_rotation(next_face, True)
    cube.make_rotation(back_face, True)
    cube.make_rotation(prev_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(prev_face, False)
    cube.make_rotation(back_face, False)
    cube.make_rotation(next_face, False)


def f2l_16(cube, next_face, current):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)


def f2l_17(cube, next_face):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_18(cube, current):
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)


def f2l_19(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, False)


def f2l_20(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(current, False)
    cube.make_rotation(next_face, True)


def f2l_21(cube, next_face):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_22(cube, prev_face, current):
    cube.make_rotation(current, False)
    cube.make_rotation(prev_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(prev_face, True)
    cube.make_rotation(current, True)


def f2l_23(cube, next_face):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)


def f2l_24(cube, next_face, current, prev_face):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(prev_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(prev_face, True)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_25(cube , next_face, current):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_26(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)


def f2l_27(cube, next_face, current):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, False)


def f2l_28(cube, next_face, current):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, False)

    cube.make_rotation(current, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(current, False)
    cube.make_rotation(next_face, True)


def f2l_29(cube, next_face, current):
    for _ in range(2):
        cube.make_rotation(next_face, False)
        cube.make_rotation(current, True)
        cube.make_rotation(next_face, True)
        cube.make_rotation(current, False)


def f2l_30(cube, next_face):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, False)

    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_31(cube, next_face, current):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)


def f2l_32(cube, next_face):
    for _ in range(2):
        cube.make_rotation(next_face, True)
        cube.make_rotation(FaceDirection.UP, True)
        cube.make_rotation(next_face, False)
        cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_33(cube, next_face):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)


def f2l_34(cube, current):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)


def f2l_35(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)


def f2l_36(cube, next_face, current):
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(current, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_38(cube, next_face, current):
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(current, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)


def f2l_39(cube, next_face):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)

    cube.make_rotation(FaceDirection.UP, False)

    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)

    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)

    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)


def f2l_40(cube, next_face):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)

    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(FaceDirection.UP, True)

    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, False)
    cube.make_rotation(next_face, False)


def f2l_41(cube, next_face, current):
    cube.make_rotation(next_face, True)
    cube.make_rotation(current, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)
    cube.make_rotation(current, False)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)


def f2l_42(cube, next_face, prev_face, current):
    cube.make_rotation(next_face, True)
    cube.make_rotation(FaceDirection.UP, False)
    cube.make_rotation(next_face, False)

    cube.make_rotation(current, False)
    cube.make_rotation(prev_face, False)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(FaceDirection.UP, True)
    cube.make_rotation(prev_face, True)
    cube.make_rotation(current, True)


