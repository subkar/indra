""" Detailed mehanistic model of BRAF based on Neal Rossen paper. """
from pysb import *
from pysb.util import alias_model_components


def monomers():
    Monomer('BRAF', ['ras', 'd', 'vem', 'erk'])
    Monomer('KRAS', ['raf'])
    Monomer('Vem', ['raf'])

    # IC values
    # --------
    Parameter('BRAF_0', 1e5)
    Parameter('KRAS_0', 2e5)
    Parameter('Vem_0', 1e5)

    alias_model_components()

    # Initial conditions
    # ------------------
    Initial(BRAF(d=None, ras=None, erk=None, vem=None), BRAF_0)
    Initial(KRAS(raf=None), KRAS_0)
    Initial(Vem(raf=None), Vem_0)


def BRAF_dynamics():
    # Parameters
    # -----------
    Parameter('kaf', 1e-6)  # 0.0001)
    Parameter('kar', 1)
    Parameter('kbf', 1)
    Parameter('kbr', 1e-11)
    Parameter('kcf', 1)
    Parameter('kcr', 0.0001)
    Parameter('kdf', 1)
    Parameter('kdr', 0.1)
    Parameter('kef', 1e-2)
    Parameter('ker', 0.1)
    Parameter('kff', 1e-5)
    Parameter('kfr', 1)
    Parameter('kgf', 1e-11)
    Parameter('kgr', 1)
    Parameter('khf', 1e-2)  # 100)
    Parameter('khr', 1)  # 1)

    alias_model_components()

    # Rules
    # -----

    # BRAF dimerization
    Rule('BRAF_dimerization',
         BRAF(d=None, ras=None) + BRAF(d=None, ras=None, vem=None) <>
         BRAF(d=1, ras=None) % BRAF(d=1, ras=None, vem=None), kaf, kar)

    # KRAS binding BRAF monomers
    Rule('KRAS_binding_BRAF_monomers',
         BRAF(ras=None, d=None) + KRAS(raf=None) <>
         BRAF(ras=1, d=None) % KRAS(raf=1), kdf, kdr)

    # KRAS binding BRAF dimers
    Rule('KRAS_binding_BRAF_dimers',
         BRAF(ras=None, d=1) % BRAF(ras=None, d=1) +
         KRAS(raf=None) + KRAS(raf=None) <>
         BRAF(ras=2, d=1) % BRAF(ras=3, d=1) %
         KRAS(raf=2) % KRAS(raf=3), kbf, kbr)

    # KRAS:BRAF dimerization
    Rule('KRASBRAF_dimerization',
         BRAF(d=None, ras=ANY) + BRAF(d=None, ras=ANY, vem=None) <>
         BRAF(d=1, ras=ANY) % BRAF(d=1, ras=ANY, vem=None), kcf, kcr)

    # BRAF:Vem dimerization to give 2(BRAF:Vem) g = a * f
    Rule('BRAF_Vem_dimerization',
         BRAF(d=None, ras=None, vem=ANY) + BRAF(d=None, ras=None, vem=ANY) <>
         BRAF(d=1, ras=None, vem=ANY) % BRAF(d=1, ras=None, vem=ANY), kgf, kgr)

    # KRAS:BRAF:Vem dimerization to give 2( KRAS:BRAF:Vem) h = c * a
    Rule('KRAS_BRAF_Vem_dimerization',
         BRAF(d=None, ras=ANY, vem=ANY) + BRAF(d=None, ras=ANY, vem=ANY) <>
         BRAF(d=1, ras=ANY, vem=ANY) % BRAF(d=1, ras=ANY, vem=ANY), khf, khr)

    # 1st Vemurafenib binds
    Rule('First_binding_Vemurafenib',
         BRAF(vem=None) % BRAF(vem=None) + Vem(raf=None) <>
         BRAF(vem=1) % BRAF(vem=None) % Vem(raf=1), kef, ker)

    # 2nd Vemurafenib binding
    Rule('Second_binding_vemurafenib',
         BRAF(vem=None) % BRAF(vem=ANY) + Vem(raf=None) <>
         BRAF(vem=1) % BRAF(vem=ANY) % Vem(raf=1), kff, kfr)

    # Vemurafenib binds BRAF monomer
    Rule('Vemurafenib_binds_BRAF_monomer',
         BRAF(vem=None, d=None) + Vem(raf=None) <>
         BRAF(vem=1, d=None) % Vem(raf=1), kef, ker)


def declare_observables():
    # Observables
    # ----------
    Observable('BRAF_WT_active',
               BRAF(d=ANY, vem=None)) 

    Observable('BRAF_V600E_active',
               BRAF(vem=None)) 

# if __name__ == '__main__':

#     from pysb.integrate import Solver
#     import matplotlib.pyplot as plt
#     import numpy as np
#     ts = np.linspace(0, 100, 100)
#     solver = Solver(model, ts)
#     solver.run()

#     plt.figure()
#     plt.plot(ts, solver.yobs['BRAF_WT_active'], label='WT')
#     plt.plot(ts, solver.yobs['BRAF_V600E_active'], label='V600E')
#     plt.legend()
#     plt.show()
