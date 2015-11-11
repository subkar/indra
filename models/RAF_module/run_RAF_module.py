# Run RAF module using different initial conditions
# for Ras and Vemurafenib levels

from BRAF_module import model
import numpy as np
from pysb.integrate import Solver

Ras_range = 2 * np.logspace(0, 3, num=20)
Vemurafenib_range = 2 * np.logspace(0, 3, num=40)

RAF_WT_level = []
RAF_V600E_level = []

for r in Ras_range:
    wt_holder_row = []
    v600e_holder_row = []
    for v in Vemurafenib_range:

        model.parameters['KRAS_0'].value = r
        model.parameters['Vem_0'].value = v

        ts = np.linspace(0, 100, 100)
        solver = Solver(model, ts)
        solver.run()

        wt_holder_row.append(solver.yobs['BRAF_WT_active'][-1])
        v600e_holder_row.append(solver.yobs['BRAF_V600E_active'][-1])

    RAF_WT_level.append(wt_holder_row)
    RAF_V600E_level.append(v600e_holder_row)

wt = np.array(RAF_WT_level, dtype='float')
v600e = np.array(RAF_V600E_level, dtype='float')


# Plots
# -----
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2)

wt_c = ax1.pcolor(Vemurafenib_range, Ras_range, wt, vmin=0, vmax=1000)
mut_c = ax2.pcolor(Vemurafenib_range, Ras_range, v600e, vmin=0, vmax=1000)

ax1.set_xlabel('Vemurafenib')
ax2.set_xlabel('Vemurafenib')
ax1.set_ylabel('Ras')
ax1.set_title('WT')
ax2.set_title('V600E')

plt.colorbar(wt_c, ax=ax1)
plt.colorbar(mut_c, ax=ax2)

plt.show()
