import numpy as np
import matplotlib.pyplot as plt
from pysb.integrate import Solver
import assemble_model

def simulate_vemurafenib_treatment(model):
    sim_hours = 10
    t = np.linspace(0, sim_hours*3600, sim_hours*60)

    model.parameters['VEMURAFENIB_0'].value = 0

    solver = Solver(model, t)
    solver.run()
    yobs1 = solver.yobs
    # New initial conditions for simulation post event
    y_init = solver.y[-1]
    y_init[model.observables['Vem_obs'].species[0]] = 2e5

    # Continue model simulation with y_init as new initial condition
    solver = Solver(model, t)
    solver.run(y0=y_init)
    yobs2 = solver.yobs

    # Concatenate the two simulations
    yobs = np.concatenate((yobs1[:-1], yobs2), axis=0)
    tout = np.append(t[:-1], t + t[-1])
    treatment_time = sim_hours*60-1
    return tout, yobs, treatment_time

def plot_fold_change_time(t, yobs, treatment_time, save_plot):
    plt.figure()
    erk_foldchange = yobs['ERK_p'][treatment_time:] / \
                     yobs['ERK_p'][treatment_time]
    ras_foldchange = yobs['RAS_active'][treatment_time:] / \
                     yobs['RAS_active'][treatment_time]
    ts = t[treatment_time:] - t[treatment_time]
    plt.plot(ts, erk_foldchange, linewidth=5)
    plt.plot(ts, ras_foldchange, linewidth=5)
    plt.xticks([])
    plt.xlabel('time (a.u)', fontsize=15)
    plt.ylabel('Fold-change after Vemurafenib treatment', fontsize=15)
    plt.xlim([0, 30000])
    plt.legend(['ERK_p', 'RAS_active', 'BRAF_active'])
    plt.savefig(save_plot)

if __name__ == '__main__':
    model_id = 1
    model = assemble_model.assemble_model(model_id)
    t, y, treatment_time = simulate_vemurafenib_treatment(model)
    plot_fold_change_time(t, y, treatment_time, 
                          'outputs/model%s_vem_treatment.png' % model_id)
