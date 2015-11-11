""" Detailed mehanistic model of BRAF based on Neal Rossen paper. """
from pysb import *

Model()

Monomer('RAF', ['ras', 'd', 'vem'])
Monomer('Ras', ['raf'])
Monomer('Vem', ['raf'])

# Parameters
# -----------
Parameter('kaf', 0.0001)
Parameter('kar', 1)
Parameter('kbf', 1)
Parameter('kbr', 1e-9)
Parameter('kcf', 1)
Parameter('kcr', 0.0001)
Parameter('kdf', 1)
Parameter('kdr', 0.1)
Parameter('kef', 1)
Parameter('ker', 0.1)
Parameter('kff', 0.001)
Parameter('kfr', 1)
Parameter('kgf', 1e-7)
Parameter('kgr', 1)
Parameter('khf', 1)  # 100)
Parameter('khr', 1)  # 1)

# IC values
# --------
Parameter('RAF_0', 1e3)
Parameter('Ras_0', 100)
Parameter('Vem_0', 1000)

# Initial conditions
# ------------------
Initial(RAF(d=None, ras=None, vem=None), RAF_0)
Initial(Ras(raf=None), Ras_0)
Initial(Vem(raf=None), Vem_0)

# Rules
# -----

# RAF dimerization
Rule('RAF_dimerization',
     RAF(d=None, ras=None) + RAF(d=None, ras=None, vem=None) <>
     RAF(d=1, ras=None) % RAF(d=1, ras=None, vem=None), kaf, kar)

# Ras binding RAF monomers
Rule('Ras_binding_RAF_monomers',
     RAF(ras=None, d=None) + Ras(raf=None) <>
     RAF(ras=1, d=None) % Ras(raf=1), kdf, kdr)

# Ras binding RAF dimers
Rule('Ras_binding_RAF_dimers',
     RAF(ras=None, d=1) % RAF(ras=None, d=1) +
     Ras(raf=None) + Ras(raf=None) <>
     RAF(ras=2, d=1) % RAF(ras=3, d=1) %
     Ras(raf=2) % Ras(raf=3), kbf, kbr)

# Ras:RAF dimerization
Rule('RasRAF_dimerization',
     RAF(d=None, ras=ANY) + RAF(d=None, ras=ANY, vem=None) <>
     RAF(d=1, ras=ANY) % RAF(d=1, ras=ANY, vem=None), kcf, kcr)

# RAF:Vem dimerization to give 2(RAF:Vem) g = a * f
Rule('RAF_Vem_dimerization',
     RAF(d=None, ras=None, vem=ANY) + RAF(d=None, ras=None, vem=ANY) <>
     RAF(d=1, ras=None, vem=ANY) % RAF(d=1, ras=None, vem=ANY), kgf, kgr)

# Ras:RAF:Vem dimerization to give 2( Ras:RAF:Vem) h = c * a
Rule('RasRAF_Vem_dimerization',
     RAF(d=None, ras=ANY, vem=ANY) + RAF(d=None, ras=ANY, vem=ANY) <>
     RAF(d=1, ras=ANY, vem=ANY) % RAF(d=1, ras=ANY, vem=ANY), khf, khr)

# 1st Vemurafenib binds
Rule('First_binding_Vemurafenib',
     RAF(vem=None) % RAF(vem=None) + Vem(raf=None) <>
     RAF(vem=1) % RAF(vem=None) % Vem(raf=1), kef, ker)

# 2nd Vemurafenib binding
Rule('Second_binding_vemurafenib',
     RAF(vem=None) % RAF(vem=ANY) + Vem(raf=None) <>
     RAF(vem=1) % RAF(vem=ANY) % Vem(raf=1), kff, kfr)

# Vemurafenib binds RAF monomer
Rule('Vemurafenib_binds_RAF_monomer',
     RAF(vem=None, d=None) + Vem(raf=None) <>
     RAF(vem=1, d=None) % Vem(raf=1), kef, ker)

# Observables
# ----------
Observable('BRAF_WT_active',
           RAF(d=ANY, vem=None)) 

Observable('BRAF_V600E_active',
           RAF(vem=None)) 

if __name__ == '__main__':

    from pysb.integrate import Solver
    import matplotlib.pyplot as plt
    import numpy as np
    ts = np.linspace(0, 100, 100)
    solver = Solver(model, ts)
    solver.run()

    plt.figure()
    plt.plot(ts, solver.yobs['BRAF_WT_active'], label='WT')
    plt.plot(ts, solver.yobs['BRAF_V600E_active'], label='V600E')
    plt.legend()
    plt.show()
