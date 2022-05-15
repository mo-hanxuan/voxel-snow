from scene import Scene
import taichi as ti
from taichi.math import *
from dendrite import Dendrite

SIZE = 256


def init_phi(anisoMode=6, angle0=0., steps=2049):
    return Dendrite(n=SIZE, dtype=ti.f32, anisoMode=anisoMode, angle0=angle0).getDendritic(steps=steps)


@ti.func
def dot_product(vec1, vec2):
    res = 0.
    for i in ti.static(range(vec1.n)):
        res += vec1[i] * vec2[i]
    return res


@ti.kernel
def make_voxels_from_field():
    bright, dark = 0.7, 0.
    for i, j in thePhi:
        if thePhi[i, j] > 0.99:  # can choose 0.99 or 0.9, bigger value relates to thicker snow-boundary
            scene.set_voxel(ivec3(i - SIZE//2, j - SIZE//2, 0), 1, vec3(0.7, 0.7, 0.7))
        elif thePhi[i, j] > 1.e-3:
            scene.set_voxel(ivec3(i - SIZE//2, j - SIZE//2, 0), 2, 
                            vec3(0.0, (dark + (bright - dark) * thePhi[i, j]) / 2., dark + (bright - dark) * thePhi[i, j]))


@ti.kernel
def set_background():
    bgSize = 300
    brightness = 0.2
    for i, j in ti.ndrange((-bgSize//2, bgSize//2), (-bgSize//2, bgSize//2)):
        # scene.set_voxel(ivec3(i, j, -bgSize//2), 1, vec3(brightness, brightness, brightness))
        scene.set_voxel(ivec3(i, -bgSize//2, j), 1, vec3(brightness, brightness, brightness))
        scene.set_voxel(ivec3(-bgSize//2, i, j), 1, vec3(brightness, brightness, brightness))


if __name__ == "__main__":

    scene = Scene(exposure=10)
    scene.set_floor(-SIZE//2, (0.2, 0.2, 0.2))
    scene.set_background_color((0., 0., 0.))
    scene.set_directional_light(vec3(0.4, 0.4, 0.4), 0.2, vec3(0.3, 0.3, 0.3))

    # thePhi = init_phi(anisoMode=4, angle0=0., steps=1800)
    thePhi = init_phi(anisoMode=6, angle0=0., steps=2048)
    make_voxels_from_field()
    set_background()

    scene.finish()
