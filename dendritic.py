"""
    Here the phase field model of dendritic solidification refer to this thesis:
        Kobayashi, R. (1993), "Modeling and numerical simulations of dendritic crystal growth." 
        Physica D 63(3-4): 410-423
    
    a larger delta (anisotropic strength) can force the snow to grow on specific direction, 
    hence can give a more beautiful morphology
"""

import taichi as ti
import numpy as np
# ti.init(arch=ti.cuda)


@ti.data_oriented
class Dendritic:
    def __init__(self, dx=0.03, n=512, dtype=ti.f64):
        self.n = n
        self.phi = ti.field(dtype=dtype, shape=(n, n))
        self.phiNew = ti.field(dtype=dtype, shape=(n, n))
        self.tp = ti.field(dtype=dtype, shape=(n, n))  # temperature
        self.tpNew = ti.field(dtype=dtype, shape=(n, n))
        self.dEnergy_dGrad_term1 = ti.Vector.field(2, dtype, shape=(n, n))  # the firat term of the energy-derivative with respect to phi_grad
        self.epsilons = ti.field(dtype=dtype, shape=(n, n))

        self.dx = dx
        self.dt = 3.e-4
        self.tau = 3.e-4

        self.epsilonbar = 0.005  # 0.005 gradient energy coefficient
        self.mu = 1.0
        self.k = 1.5   # 1.5 latent heat coefficient
        self.delta = 0.12  # 0.02 the strength of anisotropy
        self.anisoMod = 6.   # mode number of anisotropy
        self.alpha = 0.9 / np.pi  # 0.9 ^( *)([a-zA-Z])
        self.gamma = 10.0
        self.teq = 1.0  # temperature of equilibrium
        self.mo = 1. / self.tau  # mobility
        self.angle0 = 0.  # np.pi / 18. * 1.5
        self.showFrameFrequency = 16
        self.writeImages = "n"


    @ti.func
    def sumVec(self, vec):
        res = 0.
        for i in ti.static(range(vec.n)):
            res += vec[i]
        return res


    @ti.kernel
    def initializeVariables(self, ):
        radius = 1.
        center = ti.Vector([self.n//2, self.n//2])
        for i, j in self.phi:
            if self.sumVec((ti.Vector([i, j]) - center)**2) < radius**2:
                self.phi[i, j] = 1.
            else:
                self.phi[i, j] = 0.
            self.tp[i, j] = 0.  # temperature


    @ti.func
    def neighbor_index(self, i, j):
        """
            use periodic boundary condition to get neighbor index
        """
        im = i - 1 if i - 1 >= 0 else self.n - 1
        jm = j - 1 if j - 1 >= 0 else self.n - 1
        ip = i + 1 if i + 1 < self.n else 0
        jp = j + 1 if j + 1 < self.n else 0
        return im, jm, ip, jp


    @ti.func
    def divergence_dEnergy_dGrad_term1(self, i, j):
        im, jm, ip, jp = self.neighbor_index(i, j)
        return (self.dEnergy_dGrad_term1[ip, j][0] - self.dEnergy_dGrad_term1[im, j][0]) / (2. * self.dx) + \
            (self.dEnergy_dGrad_term1[i, jp][1] - self.dEnergy_dGrad_term1[i, jm][1]) / (2. * self.dx)


    @ti.kernel
    def get_epsilons_and_dEnergy_dGrad_term1(self, ):
        for i, j in self.phi:
            im, jm, ip, jp = self.neighbor_index(i, j)
            grad = ti.Vector([
                (self.phi[ip, j] - self.phi[im, j]) / (2. * self.dx), 
                (self.phi[i, jp] - self.phi[i, jm]) / (2. * self.dx)
            ])
            gradNorm = self.sumVec(grad**2)
            if gradNorm < 1.e-8:
                self.dEnergy_dGrad_term1[i, j] = ti.Vector([0., 0.])
                angle = ti.atan2(grad[1], grad[0])
                self.epsilons[i, j] = self.epsilonbar * (1. + self.delta * ti.cos(self.anisoMod * (angle - self.angle0)))
            else:
                angle = ti.atan2(grad[1], grad[0])
                epsilon = self.epsilonbar * (1. + self.delta * ti.cos(self.anisoMod * (angle - self.angle0)))
                self.epsilons[i, j] = epsilon
                dAngle_dGradX = -grad[1] / gradNorm
                dAngle_dGradY = grad[0] / gradNorm
                tmp = self.epsilonbar * self.delta * -ti.sin(self.anisoMod * (angle - self.angle0)) * self.anisoMod
                dEpsilon_dGrad = tmp * ti.Vector([dAngle_dGradX, dAngle_dGradY])
                self.dEnergy_dGrad_term1[i, j] = epsilon * dEpsilon_dGrad * gradNorm


    @ti.kernel
    def evolution(self, ):
        """get self.phi and temperature at next step"""
        for i, j in self.phi:
            im, jm, ip, jp = self.neighbor_index(i, j)

            lapla_phi = (  # laplacian of phi
                2 * (self.phi[im, j] + self.phi[i, jm] + self.phi[ip, j] + self.phi[i, jp]) 
                + (self.phi[im, jm] + self.phi[im, jp] + self.phi[ip, jm] + self.phi[ip, jp]) 
                - 12 * self.phi[i, j]
            ) / (3. * self.dx * self.dx)
            lapla_tp = (  # laplacian of temperature
                2 * (self.tp[im, j] + self.tp[i, jm] + self.tp[ip, j] + self.tp[i, jp]) 
                + (self.tp[im, jm] + self.tp[im, jp] + self.tp[ip, jm] + self.tp[ip, jp]) 
                - 12 * self.tp[i, j]
            ) / (3. * self.dx * self.dx)

            m_chem = self.alpha * ti.atan2(self.gamma * (self.teq - self.tp[i, j]), 1.)
            chemicalForce = self.phi[i, j] * (1. - self.phi[i, j]) * (self.phi[i, j] - 0.5 + m_chem)
            gradForce_term1 = self.divergence_dEnergy_dGrad_term1(i, j)
            grad_epsilon2 = ti.Vector([
                (self.epsilons[ip, j]**2 - self.epsilons[im, j]**2) / (2. * self.dx),
                (self.epsilons[i, jp]**2 - self.epsilons[i, jm]**2) / (2. * self.dx),
            ])
            grad_phi = ti.Vector([
                (self.phi[ip, j] - self.phi[im, j]) / (2. * self.dx), 
                (self.phi[i, jp] - self.phi[i, jm]) / (2. * self.dx)
            ])
            gradForce_term2 = grad_epsilon2[0] * grad_phi[0] + \
                    grad_epsilon2[1] * grad_phi[1] + \
                    self.epsilons[i, j]**2 * lapla_phi

            phiRate = self.mo * (chemicalForce + gradForce_term1 + gradForce_term2)
            self.phiNew[i, j] = self.phi[i, j] + phiRate * self.dt

            ### update the temperature
            tpRate = lapla_tp + self.k * phiRate
            self.tpNew[i, j] = self.tp[i, j] + tpRate * self.dt


    @ti.kernel
    def updateVariables(self, ):
        for i, j in self.phi:
            self.phi[i, j] = self.phiNew[i, j]
            self.tp[i, j] = self.tpNew[i, j]


    def substeps(self, ):
        self.get_epsilons_and_dEnergy_dGrad_term1()
        self.evolution()
        self.updateVariables()


    def getDendritic(self, ):
        self.initializeVariables()
        gui_tp = ti.GUI("temperature field", res=(self.n, self.n))
        gui_phi = ti.GUI("phase field", res=(self.n, self.n))

        for i in range(1025):
            
            if i % self.showFrameFrequency == 0:
                gui_tp.set_image(self.tp)
                gui_tp.show()
                gui_phi.set_image(self.phi)
                gui_phi.show(
                    "./pictures/{}.png".format(i) 
                        if i % (self.showFrameFrequency * 16) == 0 and self.writeImages == "y" 
                        else None
                )
        
            self.substeps()
            
        gui_phi.running, gui_tp.running = False, False
        return self.phi


if __name__ == "__main__":
    
    dendritic = Dendritic(n=512)
    dendritic.initializeVariables()
    gui_tp = ti.GUI("temperature field", res=(dendritic.n, dendritic.n))
    gui_phi = ti.GUI("phase field", res=(dendritic.n, dendritic.n))

    for i in range(1000000):
        
        if i % dendritic.showFrameFrequency == 0:
            gui_tp.set_image(dendritic.tp)
            gui_tp.show()
            gui_phi.set_image(dendritic.phi)
            gui_phi.show(
                "./pictures/{}.png".format(i) 
                    if i % (dendritic.showFrameFrequency * 16) == 0 and dendritic.writeImages == "y" 
                    else None
            )
    
        dendritic.substeps()
