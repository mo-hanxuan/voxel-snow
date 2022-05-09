from re import sub

from regex import D
from scene import Scene
import taichi as ti
from taichi.math import *
import numpy as np
from dendritic import Dendritic

SIZE = 128


def init_phi():
    return Dendritic(n=SIZE, dtype=ti.f32).getDendritic()


@ti.func
def dot_product(vec1, vec2):
    res = 0.
    for i in ti.static(range(vec1.n)):
        res += vec1[i] * vec2[i]
    return res


@ti.kernel
def make_voxels_from_field():
    for i, j in thePhi:
        if thePhi[i, j] > 0.5:
            scene.set_voxel(ivec3(i - 64, j - 64, 0), 1, vec3(0.9, 0.9, 0.9))


if __name__ == "__main__":

    scene = Scene(exposure=10)
    scene.set_floor(-63.9, (1.0, 1.0, 1.0))
    scene.set_background_color((0., 0., 0.))
    scene.set_directional_light(vec3(0.4, 0.4, 0.4), 0.2, vec3(0.5, 0.5, 0.5))

    thePhi = init_phi()
    make_voxels_from_field()

    scene.finish()
