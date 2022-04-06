from . import utils


def oll_9(front, left, right, back, up, up_color):
    return back.face_matrix[0][0] == up_color and right.face_matrix[0][1] == up_color and \
            left.face_matrix[0][0] == up_color and up.face_matrix[2][2] == up_color and \
            front.face_matrix[0][0] == up_color and front.face_matrix[0][1] == up_color


def oll_10(front, left, right, back, up, up_color):
    return front.face_matrix[0][2] == right.face_matrix[0][1] == left.face_matrix[0][2] == back.face_matrix[0][1] ==\
        back.face_matrix[0][2] == up.face_matrix[0][2] == up_color


def oll_13(front, right, back, up, up_color):
    return front.face_matrix[0][1] == front.face_matrix[0][2] == right.face_matrix[0][2] == back.face_matrix[0][1] ==\
            back.face_matrix[0][2] == up.face_matrix[2][0] == up_color


def oll_14(front, left, back, up, up_color):
    return front.face_matrix[0][0] == front.face_matrix[0][1] == left.face_matrix[0][0] == back.face_matrix[0][0] ==\
            back.face_matrix[0][1] == up.face_matrix[2][2] == up_color


def oll_17(front, left, right, back, up, up_color):
    return front.face_matrix[0][1] == right.face_matrix[0][1] == left.face_matrix[0][1] == left.face_matrix[0][2] ==\
        back.face_matrix[0][1] == back.face_matrix[0][0] == up.face_matrix[0][0] == up.face_matrix[0][2] == up_color


def oll_20(front, left, right, back, up, up_color):
    return front.face_matrix[0][1] == left.face_matrix[0][1] == right.face_matrix[0][1] == back.face_matrix[0][1] ==\
        up.face_matrix[0][0] == up.face_matrix[0][2] == up.face_matrix[2][0] == up.face_matrix[2][2] == up_color


def oll_21(front, back, up_color):
    return front.face_matrix[0][0] == front.face_matrix[0][2] == back.face_matrix[0][0] == back.face_matrix[0][2] ==\
            up_color


def oll_22(front, left, back, up_color):
    return front.face_matrix[0][2] == left.face_matrix[0][0] == left.face_matrix[0][2] == back.face_matrix[0][0] ==\
            up_color


def oll_23(back, up, up_color):
    return back.face_matrix[0][0] == back.face_matrix[0][2] == up.face_matrix[2][0] == up.face_matrix[2][2] ==\
            up_color


def oll_24(front, back, up, up_color):
    return front.face_matrix[0][0] == back.face_matrix[0][2] == up.face_matrix[0][2] == up.face_matrix[2][2] == up_color


def oll_25(front, left, up, up_color):
    return front.face_matrix[0][2] == left.face_matrix[0][0] == up.face_matrix[2][0] == up.face_matrix[0][2] == up_color


def oll_26(front, left, right, up, up_color):
    return front.face_matrix[0][0] == left.face_matrix[0][0] == right.face_matrix[0][0] == up.face_matrix[0][2] == up_color


def oll_27(front, right, back, up, up_color):
    return front.face_matrix[0][2] == right.face_matrix[0][2] == back.face_matrix[0][2] == up.face_matrix[2][0] == up_color


def oll_28(front, right, up, up_color):
    return front.face_matrix[0][1] == right.face_matrix[0][1] == up.face_matrix[0][0] == up.face_matrix[0][2] ==\
            up.face_matrix[2][0] == up.face_matrix[2][2] == up_color


def oll_29(front, right, back, up, up_color):
    return back.face_matrix[0][2] == up_color and front.face_matrix[0][0] and \
            right.face_matrix[0][1] == up_color and front.face_matrix[0][1] == up_color and \
            up.face_matrix[0][2] == up_color and up.face_matrix[2][2] == up_color


def oll_30(front, left, right, up, up_color):
    return front.face_matrix[0][1] == left.face_matrix[0][0] == right.face_matrix[0][1] == right.face_matrix[0][2] ==\
            up.face_matrix[2][0] == up.face_matrix[2][2] == up_color


def oll_31(front, left, back, up, up_color):
    return front.face_matrix[0][0] == front.face_matrix[0][1] == left.face_matrix[0][1] == back.face_matrix[0][2] ==\
            up.face_matrix[0][2] == up.face_matrix[2][2] == up_color


def oll_32(front, right, back, up, up_color):
    return front.face_matrix[0][2] == right.face_matrix[0][1] == back.face_matrix[0][0] == up.face_matrix[0][0] ==\
            up.face_matrix[2][0] == up_color


def oll_33(front, back, up, up_color):
    return up.face_matrix[2][2] == up_color and up.face_matrix[0][2] == up_color and \
            back.face_matrix[0][1] == up_color and back.face_matrix[0][2] == up_color and \
            front.face_matrix[0][0] == up_color and front.face_matrix[0][1] == up_color


def oll_34(front, left, right, back, up, up_color):
    return up.face_matrix[2][0] == up.face_matrix[2][2] == front.face_matrix[0][1] == back.face_matrix[0][1] ==\
            left.face_matrix[0][0] == right.face_matrix[0][2] == up_color


def oll_35(front, left, right, back, up, up_color):
    return up.face_matrix[2][2] == up.face_matrix[0][0] == front.face_matrix[0][0] == right.face_matrix[0][2] ==\
            left.face_matrix[0][1] == back.face_matrix[0][1] == up_color


def oll_36(front, left, back, up, up_color):
    return up.face_matrix[0][0] == up_color and up.face_matrix[2][2] == up_color and \
            front.face_matrix[0][1] == up_color and back.face_matrix[0][0] == up_color and \
            left.face_matrix[0][1] == up_color and left.face_matrix[0][2] == up_color


def oll_37(front, right, up, up_color):
    return up.face_matrix[0][0] == up_color and up.face_matrix[2][2] and \
            right.face_matrix[0][1] == up_color and right.face_matrix[0][2] and \
            front.face_matrix[0][0] == up_color and front.face_matrix[0][1]


def oll_38(front, right, back, up, up_color):
    return up.face_matrix[0][2] == up_color and up.face_matrix[2][0] == up_color and \
            right.face_matrix[0][1] == up_color and right.face_matrix[0][0] == up_color and \
            front.face_matrix[0][1] == up_color and back.face_matrix[0][2] == up_color


def oll_39(front, right, back, up, up_color):
    return up.face_matrix[0][2] == up.face_matrix[2][0] == front.face_matrix[0][1] == right.face_matrix[0][0] ==\
            back.face_matrix[0][1] == back.face_matrix[0][2] == up_color


def oll_40(front, left, back, up, up_color):
    return up.face_matrix[0][0] == up.face_matrix[2][2] == front.face_matrix[0][1] == left.face_matrix[0][2] ==\
            back.face_matrix[0][1] == back.face_matrix[0][0] == up_color


def oll_41(front, right, back, up, up_color):
    return up.face_matrix[2][0] == up.face_matrix[2][2] == front.face_matrix[0][1] == right.face_matrix[0][1] ==\
            back.face_matrix[0][0] == back.face_matrix[0][2] == up_color


def oll_42(front, right, back, up, up_color):
    return front.face_matrix[0][0] == front.face_matrix[0][2] == right.face_matrix[0][1] == back.face_matrix[0][1] ==\
        up.face_matrix[0][0] == up.face_matrix[0][2] == up_color


def oll_43(front, left, up, up_color):
    return utils.line_in_single_color(left, 0, up_color) and front.face_matrix[0][1] == up.face_matrix[0][2] ==\
            up.face_matrix[2][2] == up_color


def oll_44(front, right, up, up_color):
    return utils.line_in_single_color(right, 0, up_color) and front.face_matrix[0][1] == up.face_matrix[2][0] ==\
            up.face_matrix[0][0] == up_color


def oll_45(front, left, back, up, up_color):
    return up.face_matrix[0][2] == up_color and up.face_matrix[2][2] == up_color and \
            front.face_matrix[0][1] == up_color and back.face_matrix[0][1] == up_color and \
            left.face_matrix[0][0] == up_color and left.face_matrix[0][2] == up_color


def oll_46(left, right, up, up_color):
    return utils.line_in_single_color(right, 0, up_color) and left.face_matrix[0][1] == up.face_matrix[0][0] ==\
        up.face_matrix[2][0] == up_color


def oll_47(front, left, right, back, up_color):
    return front.face_matrix[0][0] == front.face_matrix[0][1] == left.face_matrix[0][1] == right.face_matrix[0][0] ==\
            right.face_matrix[0][2] == back.face_matrix[0][2] == up_color


def oll_48(front, left, right, back, up_color):
    return front.face_matrix[0][1] == front.face_matrix[0][2] == back.face_matrix[0][0] == right.face_matrix[0][1] ==\
            left.face_matrix[0][0] == left.face_matrix[0][2] == up_color


def oll_49(front, right, back, up_color):
    return utils.line_in_single_color(right, 0, up_color) and front.face_matrix[0][0] == back.face_matrix[0][1] ==\
            back.face_matrix[0][2] == up_color


def oll_50(front, left, back, up_color):
    return utils.line_in_single_color(left, 0, up_color) and front.face_matrix[0][2] == back.face_matrix[0][1] ==\
        back.face_matrix[0][0] == up_color


def oll_52(front, left, right, back, up_color):
    return utils.line_in_single_color(right, 0, up_color) and front.face_matrix[0][0] == back.face_matrix[0][2] ==\
            left.face_matrix[0][1] == up_color


def oll_55(front, back, up_color):
    return utils.line_in_single_color(front, 0, up_color) and utils.line_in_single_color(back, 0, up_color)


def oll_56(front, left, right, back, up_color):
    return front.face_matrix[0][1] == back.face_matrix[0][1] == left.face_matrix[0][0] == left.face_matrix[0][2] ==\
        right.face_matrix[0][0] == right.face_matrix[0][2] == up_color