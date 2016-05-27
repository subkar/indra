def run_model(model, save_plot='model_plot.png'):
    
    from pysb.integrate import Solver
    import numpy as np    
    #from model import model

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

    plt.plot(t, yobs2['ERK_p']/yobs2['ERK_p'][0],
             t, yobs2['RAS_active']/yobs2['RAS_active'][0], linewidth=5)
    plt.savefig(save_plot)
