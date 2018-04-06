# coding=utf-8

import random
from OpenGL.GL import glCallList, glColor3f, glMaterialfv, glMultMatrixf, glPopMatrix, glPushMatrix, \
                      GL_EMISSION, GL_FRONT
import numpy
import color
from primitive import G_OBJ_SPHERE, G_OBJ_CUBE
from transformation import scaling, translation
from aabb import AABB


class Node(object):
    def __init__(self):
        # 该节点的颜色序号
        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)
        # 该节点的平移矩阵
        self.translation_matrix = numpy.identity(4)
        # 该节点的缩放矩阵
        self.scaling_matrix = numpy.identity(4)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.selected = False

    def render(self):
        """
        渲染节点
        :return:
        """
        glPushMatrix()
        # 平移
        glMultMatrixf(numpy.transpose(self.translation_matrix))
        # 缩放
        glMultMatrixf(self.scaling_matrix)
        cur_color = color.COLORS[self.color_index]
        # 设置颜色
        glColor3f(cur_color[0], cur_color[1], cur_color[2])
        if self.selected: # 选中的对象会发光
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.3, 0.3])
        # 渲染对象模型
        self.render_self()
        if self.selected: # 选中的对象会发光
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])
        glPopMatrix()

    def render_self(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'render_self'"
        )

    def select(self, select=None):
        if select is not None:
            self.selected = select
        else:
            self.selected = not self.selected

    def pick(self, start, direction, mat):
        # 将modelview矩阵乘上节点的变换矩阵
        newmat = numpy.dot(
            numpy.dot(mat, self.translation_matrix),
            numpy.linalg.inv(self.scaling_matrix)
        )
        results = self.aabb.ray_hit(start, direction, newmat)
        return results

    def translate(self, x, y, z):
        self.translation_matrix = numpy.dot(self.translation_matrix, translation([x, y, z]))

    def scale(self, s):
        self.scaling_matrix = numpy.dot(self.scaling_matrix, scaling([s, s, s]))


class Primitive(Node):
    def __init__(self):
        super(Primitive, self).__init__()
        self.call_list = None

    def render_self(self):
        glCallList(self.call_list)


class Sphere(Primitive):
    """
    球形图元
    """
    def __init__(self):
        super(Sphere, self).__init__()
        self.call_list = G_OBJ_SPHERE


class Cube(Primitive):
    """
    立方体图元
    """
    def __init__(self):
        super(Cube, self).__init__()
        self.call_list = G_OBJ_CUBE

class HierarchicalNode(Node):
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()


class SnowFigure(HierarchicalNode):
    def __init__(self):
        super(SnowFigure, self).__init__()
        self.child_nodes = [Sphere(), Sphere(), Sphere()]
        self.child_nodes[0].translate(0, -0.6, 0)
        self.child_nodes[1].translate(0, 0.1, 0)
        self.child_nodes[1].scale(0.8)
        self.child_nodes[2].translate(0, 0.75, 0)
        self.child_nodes[2].scale(0.7)
        for child_node in self.child_nodes:
            child_node.color_index = color.MIN_COLOR


