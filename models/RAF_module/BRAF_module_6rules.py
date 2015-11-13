""" Detailed mehanistic model of BRAF based on Neal Rossen paper.
This module has fewer rules """
from pysb import *
from pysb.util import alias_model_components


def monomers():
    Monomer('BRAF', ['ras', 'd', 'vem', 'erk'])
    Monomer('KRAS', ['raf'])
    Monomer('Vem', ['raf'])

    # IC values
    # --------
    Parameter('BRAF_0', 1e3)
    Parameter('KRAS_0', 100)
    Parameter('Vem_0', 0)

    alias_model_components()

    # Initial conditions
    # ------------------
    Initial(BRAF(d=None, ras=None, vem=None, erk=None), BRAF_0)
    Initial(KRAS(raf=None), KRAS_0)
    Initial(Vem(raf=None), Vem_0)


def BRAF_dynamics():

    # Parameters
    # -----------
    Parameter('kaf', 1e-4)  # 1e-5
    Parameter('kar', 1)
    Parameter('kbf', 1)
    Parameter('kbr', 1e-9)
    Parameter('kcf',  1)
    Parameter('kcr', 0.0001)
    Parameter('kdf', 1)
    Parameter('kdr', 0.1)
    Parameter('kef', 1)
    Parameter('ker', 0.1)
    Parameter('kff',  0.001)
    Parameter('kfr', 1)  # 0.1
    Parameter('kgf', 1e-7)
    Parameter('kgr', 1)
    Parameter('khf', 1)
    Parameter('khr', 1)
    Parameter('koff', 1)

    alias_model_components()

    # Rules
    # -----

    # BRAF dimerization
    Rule('BRAF_binds_BRAF',
         BRAF(d=None) + BRAF(d=None, ras=None) <>
         BRAF(d=1) % BRAF(d=1, ras=None), kaf, kar)

    # KRAS binding BRAF monomers
    Rule('KRAS_binds_BRAF',
         BRAF(ras=None) + KRAS(raf=None) <>
         BRAF(ras=1) % KRAS(raf=1), kdf, kdr)

    # KRAS:BRAF dimerization
    Rule('KRAS_BRAF_dimerization',
         BRAF(d=None, ras=ANY) + BRAF(d=None, ras=ANY) <>
         BRAF(d=1, ras=ANY) % BRAF(d=1, ras=ANY), kcf, kcr)

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
