""" Detailed mehanistic model of BRAF based on Neal Rossen paper.
This module has fewer rules """
from pysb import *
from pysb.util import alias_model_components

# Model()

Monomer('BRAF', ['ras', 'd', 'vem', 'mek'])
# Monomer('KRAS', ['raf'])
Monomer('Vem', ['raf'])

# Parameters
# -----------
Parameter('kaf', 1e-5)
Parameter('kar', 1)
Parameter('kbf', 1)
Parameter('kbr', 0.001)
Parameter('kcf',  1)
Parameter('kcr', 0.001)
Parameter('kdf', 1)
Parameter('kdr', 0.1)
Parameter('kef', 1)
Parameter('ker', 0.1)
Parameter('kff',  0.001)
Parameter('kfr', 0.1)
Parameter('kgf', 0.00001)
Parameter('kgr', 1)
Parameter('khf', 100)
Parameter('khr', 1)
Parameter('koff', 1)

# IC values
# --------
Parameter('BRAF_0', 2e4)
# Parameter('KRAS_0', 100)
Parameter('Vem_0', 0)

alias_model_components()

# Initial conditions
# ------------------
Initial(BRAF(d=None, ras=None, vem=None, mek=None), BRAF_0)
# Initial(KRAS(raf=None), KRAS_0)
Initial(Vem(raf=None), Vem_0)

# Rules
# -----

# BRAF dimerization
Rule('BRAF_binds_BRAF',
     BRAF(d=None) + BRAF(d=None, ras=None) <>
     BRAF(d=1) % BRAF(d=1, ras=None), kaf, kar)

# KRAS binding BRAF monomers
Rule('KRAS_binds_BRAF',
     BRAF(ras=None) + KRAS(raf=None, state='gtp') <>
     BRAF(ras=1) % KRAS(raf=1, state='gtp'), kdf, kdr)

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

# KRAS GDP rleased from BRAF
Rule('KRAS_GDP_unbinds',
     KRAS(state='gdp', raf=1) % BRAF(ras=1) >>
     KRAS(state='gdp', raf=None) + BRAF(ras=None), koff)


# Observables
# ----------
Observable('BRAF_WT_active',
           BRAF(d=ANY, vem=None) +
           BRAF(d=1, vem=None) % BRAF(d=1, vem=ANY))

Observable('BRAF_V600E_active',
           BRAF(d=None, vem=None) +
           BRAF(d=ANY, vem=None) +
           BRAF(d=1, vem=None) % BRAF(d=1, vem=ANY))

Observable('BRAF_dimers', BRAF(d=ANY, vem=None))

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
