import os
import pickle
import numpy as np
import matplotlib
# To suppress plots from popping up
matplotlib.use('Agg')
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
    y_init[model.observables['Vem_free'].species[0]] = 2e5

    # Continue model simulation with y_init as new initial condition
    solver = Solver(model, ts)
    solver.run(y0=y_init)

    # Concatenate the two simulations
    return solver.yobs, solver.y

def is_steady_state(y):
    for k in y.dtype.fields.keys():
        d = np.diff(y[k])
        if not all(abs(d) < max(abs(y[k]))*0.01):
            return False
    return True

def get_steady_state(model, y0):
    sim_hours = 1
    t = np.linspace(0, sim_hours*3600, sim_hours*60)
    solver = Solver(model, t)
    ss = False
    y_init = y0
    while not ss:
        solver.run(y0=y_init)
        ss = is_steady_state(solver.yobs)
        y_init = solver.y[-1]
    steady_state = solver.yobs[-1]
    return steady_state

def plot_fold_change_time(t, yobs, yobs_ref, save_plot):
    erk_foldchange = yobs['ERK_p'] / yobs_ref['ERK_p']
    ras_foldchange = yobs['RAS_active'] / yobs_ref['RAS_active']
    plt.figure()
    plt.plot(ts, erk_foldchange, linewidth=5)
    plt.plot(ts, ras_foldchange, linewidth=5)
    plt.xticks([])
    plt.xlabel('time (a.u)', fontsize=15)

    plt.xlim([0, 30000])
    plt.ylabel('Fold-change after Vemurafenib treatment', fontsize=15)
    plt.legend(['Phosphorylated ERK', 'Active RAS'])
    plt.savefig(save_plot, dpi=600)
    plt.clf()

def get_egf_vem_doseresp(egf_doses, vem_doses, readout='absolute'):
    yobs0, y0 = simulate_untreated(model, ts)
    erk = np.zeros((len(egf_doses), len(vem_doses)))
    ras = np.zeros((len(egf_doses), len(vem_doses)))
    for i, ed in enumerate(egf_doses):
        for j, vd in enumerate(vem_doses):
            y0_last = y0[-1]
            y0_last[model.observables['EGF_free'].species[0]] = ed
            y0_last[model.observables['Vem_free'].species[0]] = vd
            yobs_ss = get_steady_state(model, y0_last)
            if readout == 'absolute':
                erk[i,j] = yobs_ss['ERK_p']
                ras[i,j] = yobs_ss['RAS_active']
            elif readout == 'foldchange':
                erk[i,j] = yobs_ss['ERK_p'] / yobs0['ERK_p'][-1]
                ras[i,j] = yobs_ss['RAS_active'] / yobs0['RAS_active'][-1]
            print ed, vd, erk[i,j], ras[i,j]
            print yobs_ss['ERK_p']
            print yobs_ss['RAS_active']
    return erk, ras

def plot_egf_vem_dose(egf_doses, vem_doses, erk, ras, save_plot):
    cmap = plt.get_cmap('bwr')
    f, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(np.flipud(erk), cmap=cmap)
    ax1.set_title('pERK')
    ax1.set_xlabel('Vemurafenib')
    ax1.set_ylabel('EGF')
    ax1.set_aspect('equal')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.imshow(np.flipud(ras), cmap=cmap)
    ax2.set_title('Active RAS')
    ax2.set_xlabel('Vemurafenib')
    ax2.set_ylabel('EGF')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_aspect('equal')
    f.savefig(save_plot)

    #plt.plot(egf_doses, erk_vals, linewidth=5)
    #plt.plot(egf_doses, ras_vals, linewidth=5)
    #plt.xticks([])
    #plt.xlabel('EGF dose (a.u.)', fontsize=15)
    #plt.ylabel('Fold-change after Vemurafenib treatment', fontsize=15)
    #plt.legend(['ERK_p', 'RAS_active'])
    #plt.savefig(save_plot)

def load_model(model_id):
    model = pickle.load(open('model%d.pkl' % model_id, 'rb'))
    return model

def save_model(model):
    with open('model%d.pkl' % model_id, 'wb') as fh:
        pickle.dump(model, fh)

if __name__ == '__main__':
    sim_hours = 10
    ts = np.linspace(0, sim_hours*3600, sim_hours*60)
    egf_doses = np.logspace(4, 6, 5)
    vem_doses = np.logspace(4, 6, 5)
    for model_id in (1,2,4):
        print 'Running model %d' % model_id
        print '----------------'
        if os.path.exists('model%d.pkl' % model_id):
            model = load_model(model_id)
        else:
            model = assemble_model.assemble_model(model_id)
            generate_equations(model)
            save_model(model)
        yobs1, y1 = simulate_untreated(model, ts)
        yobs2, y2 = simulate_vemurafenib_treatment(model, ts, y1[-1])
        plot_fold_change_time(ts, yobs2, yobs1[-1],
                              'outputs/model%s_vem_time.png' % model_id)
        erk_foldchange, ras_foldchange = \
            get_egf_vem_doseresp(egf_doses, vem_doses)
        plot_egf_vem_dose(egf_doses, vem_doses,
                              erk_foldchange, ras_foldchange,
                              'outputs/model%s_egf_vem_dose.png' % model_id)
