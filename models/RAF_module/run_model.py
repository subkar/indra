import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pysb.integrate import Solver
from pysb.bng import generate_equations
import assemble_model

def simulate_untreated(model, ts):
    model.parameters['VEMURAFENIB_0'].value = 0

    solver = Solver(model, ts)
    solver.run()
    return (solver.yobs, solver.y)

def simulate_vemurafenib_treatment(model, ts, y0):
    # New initial conditions for simulation post event
    y_init = y0
    y_init[model.observables['Vem_obs'].species[0]] = 2e5

    # Continue model simulation with y_init as new initial condition
    solver = Solver(model, ts)
    solver.run(y0=y_init)

    # Concatenate the two simulations
    return solver.yobs, solver.y

def is_steady_state(y):
    for k in y.dtype.fields.keys():
        d = np.diff(y[k])
        if not all(abs(d) < max(y[k])*0.01):
            return False
    return True

def get_steady_state(model, y0):
    sim_hours = 10
    t = np.linspace(0, sim_hours*3600, sim_hours*60)
    solver = Solver(model, t)
    ss = False
    y_init = y0
    while not ss:
        solver.run(y0=y_init)
        ss = is_steady_state(solver.yobs)
        y_init = solver.y[-1]
    return solver.yobs

def plot_fold_change_time(t, yobs, yobs_ref, save_plot):
    erk_foldchange = yobs['ERK_p'] / yobs_ref['ERK_p']
    ras_foldchange = yobs['RAS_active'] / yobs_ref['RAS_active']
    plt.ion()
    plt.figure()
    plt.plot(ts, erk_foldchange, linewidth=5)
    plt.plot(ts, ras_foldchange, linewidth=5)
    plt.xticks([])
    plt.xlabel('time (a.u)', fontsize=15)
    plt.ylabel('Fold-change after Vemurafenib treatment', fontsize=15)
    #plt.xlim([0, 30000])
    plt.legend(['Phosphorylated ERK', 'Active RAS'])
    plt.savefig(save_plot)

def plot_fold_change_egfdose(egf_doses, y0, yobs_ref, save_plot):
    erk_vals = []
    ras_vals = []
    for ed in egf_doses:
        model.parameters['VEMURAFENIB_0'].value = 2e5
        model.parameters['EGF_0'].value = ed
        yobs_ss = get_steady_state(model, y0)
        erk_foldchange = yobs_ss['ERK_p'][-1] / yobs_ref['ERK_p']
        erk_vals.append(erk_foldchange)
        ras_foldchange = yobs_ss['RAS_active'][-1] / yobs_ref['RAS_active']
        ras_vals.append(ras_foldchange)
    plt.ion()
    plt.figure()
    plt.plot(egf_doses, erk_vals, linewidth=5)
    plt.plot(egf_doses, ras_vals, linewidth=5)
    plt.xticks([])
    plt.xlabel('EGF dose (a.u.)', fontsize=15)
    plt.ylabel('Fold-change after Vemurafenib treatment', fontsize=15)
    plt.legend(['ERK_p', 'RAS_active'])
    plt.savefig(save_plot)

def load_model(model_id):
    model = pickle.load('model%d.pkl' % model_id)
    return model

def save_model(model):
    with open('model%d.pkl' % model_id, 'wb') as fh:
        pickle.dump(model, fh)

if __name__ == '__main__':
    for model_id in (1,2,3,4):
        if os.path.exists('model%d.pkl' % model_id):
            model = load_model(model_id)
        else:
            model = assemble_model.assemble_model(model_id)
            generate_equations(model)
            save_model(model)
        sim_hours = 10
        ts = np.linspace(0, sim_hours*3600, sim_hours*60)
        yobs1, y1 = simulate_untreated(model, ts)
        yobs2, y2 = simulate_vemurafenib_treatment(model, ts, y1[-1])
        plot_fold_change_time(ts, yobs2, yobs1[-1],
                              'outputs/model%s_vem_time.png' % model_id)
        plot_fold_change_egfdose(np.logspace(0, 5, 10), y1[-1], yobs1[-1],
                                 'outputs/model%s_egf_dose.png' % model_id)
