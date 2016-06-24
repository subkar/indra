import numpy as np
import matplotlib.pyplot as plt
from pysb.integrate import Solver

def run_model(model, save_plot='model_plot.png'):
    t = np.linspace(0, 10*3600, 10*60)

    model.parameters['VEMURAFENIB_0'].value = 0

    solver = Solver(model, t)
    solver.run()
    y1 = solver.y
    yobs1 = solver.yobs
    # New initial conditions for simulation post event
    y_init = solver.y[-1]
    # Change level of Vemurafenib from 0 to 2e4 molecules/cell
    assert len(model.observables['Vem_obs'].species) == 1, \
        "The observable complex pattern is comprised of more than one species."

    y_init[model.observables['Vem_obs'].species[0]] = 2e5

    # Continue model simulation with y_init as new initial condition
    solver = Solver(model, t)
    solver.run(y0=y_init)
    y2 = solver.y
    yobs2 = solver.yobs

    # Concatenate the two simulations
    yout = np.concatenate((y1[:-1], y2), axis=0)
    yobs = np.concatenate((yobs1[:-1], yobs2), axis=0)
    tout = np.append(t[:-1], t + t[-1])
    
    plt.figure()
    plt.ion()
    plt.plot(t, yobs2['ERK_p']/yobs2['ERK_p'][0],
             t, yobs2['RAS_active']/yobs2['RAS_active'][0],
             linewidth=5)
    plt.xticks([])
    plt.xlabel('time (a.u)', fontsize=15)
    plt.ylabel('Fold-change after Vemurafenib treatment', fontsize=15)
    plt.xlim([0, 30000])
    plt.legend(['ERK_p', 'RAS_active', 'BRAF_active'])
    plt.savefig(save_plot)
    plt.clf()


    
