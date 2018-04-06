# coding=utf-8

import numpy


def translation(displacement):
    """
    生成平移矩阵
    :param displacement:
    :return:
    """
    t = numpy.identity(4)
    t[0, 3] = displacement[0]
    t[1, 3] = displacement[1]
    t[2, 3] = displacement[2]
    return t


def scaling(scale):
    """
    生成缩放矩阵
    :param scale:
    :return:
    """
    s = numpy.identity(4)
    s[0, 0] = scale[0]
    s[1, 1] = scale[1]
    s[2, 2] = scale[2]
    s[3, 3] = 1
    return s
