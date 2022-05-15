# <a name="title">voxel-bitSnow</a>

Numerical simulation of **snow growing** by solving **partial-differential-equations (PDEs)**. Coupling **phase field** (PF) and **temperature field** to simulate the snow growth. **Fast parallel computing** of PDE by **taichi**.

<p align="left">
<img src="https://lh3.googleusercontent.com/gp_mebbK7wEasexbIoSj9IA4eAEoEp9TpubWbcXQkvvoto3iBRcCqa2btUOH72GUndLhf9uglRBXV3BO82GakkzRijnG_vFYGCvW=s0" width="64%" align="center"></img>
</p> 


> Fig. 1. [voxel-bitSnow](https://opensea.io/assets/0x495f947276749ce646f68ac8c248420045cb7b5e/5025769837641590739412139785757932472560744325011754290274748814264725667841/) growing from numerical simulation by [Taichi](https://github.com/taichi-dev/taichi). 


<p align="left">
<img src="https://github.com/mo-hanxuan/Snow-Dendrite-Growth/blob/main/README.assets/snow_512x512.gif?raw=true" width="32%" align="center"></img>
</p> 



> Fig. 2. [bitSnow growing with 6-fold symmetry](https://opensea.io/assets/0x495f947276749ce646f68ac8c248420045cb7b5e/5025769837641590739412139785757932472560744325011754290274748799971074506753): Simulation of snow growing by solving partial-differential-equations (PDEs). **Coupling phase field (PF) and temperature field to simulate the snow growth.** Fast **parallel computing** of partial differential equation (PDE) by **taichi**. For more info, refer to [https://github.com/mo-hanxuan/Snow-Dendrite-Growth](https://github.com/mo-hanxuan/Snow-Dendrite-Growth).

## Basic ideas
Coupling between **phase field** and **temperature field**, where

1. Phase field solves spatial distribution of solid (snow) and liquid, which considers:

   + anisotropic interface energy

   + temperature-dependent chemical-potential

2. Temperature field, which considers:

   + heat conduction

   + latent heat from solidification

Get the taichi field of snow and convert it to voxels, where the voxels' colors and brightnesses are determined by field values.

We use voxels with glowing material at the boundary of the snow, and set the gray wall at left and bottom to reflect the light and shadow.   

For more info about the simulation model of snow-growing, refer to  [https://github.com/mo-hanxuan/Snow-Dendrite-Growth](https://github.com/mo-hanxuan/Snow-Dendrite-Growth).

## activities

We invite you to create your voxel artwork, by putting your [Taichi](https://github.com/taichi-dev/taichi) code in `main.py`!

Rules:

+ You can only import two modules: `taichi` (`pip` installation guide below) and `scene.py` (in the repo).
+ The code in `main.py` cannot exceed 99 lines. Each line cannot exceed 120 characters.

The available APIs are:

+ `scene = Scene(voxel_edges, exposure)`
+ `scene.set_voxel(voxel_id, material, color)`
+ `material, color = scene.get_voxel(voxel_id)`
+ `scene.set_floor(height, color)`
+ `scene.set_directional_light(dir, noise, color)`
+ `scene.set_background_color(color)`

Remember to call `scene.finish()` at last.

**Taichi Lang documentation:** https://docs.taichi-lang.org/

**Modifying files other than `main.py` is not allowed.**


## Installation

Make sure your `pip` is up-to-date:

```bash
pip3 install pip --upgrade
```

Assume you have a Python 3 environment, simply run:

```bash
pip3 install -r requirements.txt
```

to install the dependencies of the voxel renderer.

## Quickstart

```sh
python3 main.py
```

Mouse and keyboard interface:

+ Drag with your left mouse button to rotate the camera.
+ Press `W/A/S/D/Q/E` to move the camera.
+ Press `P` to save a screenshot.

## More examples

<a href="https://github.com/raybobo/taichi-voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/city.jpg" width="45%"></img></a>  <a href="https://github.com/victoriacity/voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/city2.jpg" width="45%"></img></a> 
<a href="https://github.com/yuanming-hu/voxel-art"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/tree2.jpg" width="45%"></img></a> <a href="https://github.com/neozhaoliang/voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/desktop.jpg" width="45%"></img></a> 
<a href="https://github.com/maajor/maajor-voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/earring_girl.jpg" width="45%"></img></a>  <a href="https://github.com/rexwangcc/taichi-voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/pika.jpg" width="45%"></img></a> 
<a href="https://github.com/houkensjtu/qbao_voxel_art"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/yinyang.jpg" width="45%"></img></a>  <a href="https://github.com/ltt1598/voxel-challenge"><img src="https://github.com/taichi-dev/public_files/blob/master/voxel-challenge/lang.jpg" width="45%"></img></a> 
