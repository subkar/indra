import sys
sys.path.append('../..')

from indra import trips
from indra.assemblers import PysbAssembler

tp = trips.process_text(open('vr_mut_input.txt').read())

pa = PysbAssembler()
pa.add_statements(tp.statements)
model = pa.make_model(policies='two_step')

rule1 = model.rules['BRAF_V600E_BRAF_V600E_bind']
rule2 = model.rules['BRAF_V600E_BRAF_V600E_dissociate']
rule3 = model.rules['VEMURAFENIB_BRAF_V600E_bind']
rule4 = model.rules['VEMURAFENIB_BRAF_V600E_dissociate']

from enumerate_rules import enumerate_rules

enumerate_rules(model, rule1, ['map2k1', 'V600'])
enumerate_rules(model, rule2, ['map2k1', 'V600'])
enumerate_rules(model, rule3, ['map2k1', 'nras', 'V600'])
enumerate_rules(model, rule4, ['map2k1', 'nras', 'V600'])

import pysb.export
with open('enumerated_v600e_model.py', 'w') as f:
    f.write(pysb.export.export(model, 'pysb_flat'))

from pysb.integrate import Solver
import numpy as np    
from enumerated_v600e_model import model

t = np.linspace(0, 10*3600, 10*60)

model.parameters['VEMURAFENIB_0'].value = 0

solver = Solver(model, t)
solver.run()
y1 = solver.y
yobs1 = solver.yobs
# new initial conditions for simulation post event
y_init = solver.y[-1]
# Change level of Vemurafenib from 0 to 2e4 molecules/cell
assert len(model.observables['Vem_obs'].species) == 1, \
    "The observable complex pattern is comprised of more than one species."

y_init[model.observables['Vem_obs'].species[0]] = 2e5

# continue model simulation with y_init as new initial condition
solver = Solver(model, t)
solver.run(y0=y_init)
y2 = solver.y
yobs2 = solver.yobs

# Append 
yout = np.concatenate((y1[:-1], y2), axis=0)
yobs = np.concatenate((yobs1[:-1], yobs2), axis=0)
tout = np.append(t[:-1], t + t[-1])

import matplotlib.pyplot as plt

plt.plot(tout, yobs['MAPK1_P'], linewidth=5)
plt.show()
