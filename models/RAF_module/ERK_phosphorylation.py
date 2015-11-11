""" ERK is phosphorylated (2-step catalysis) by BRAF (wt &  v600e) and CRAF """

from pysb import *
from pysb.macros import catalyze_state
from pysb.util import alias_model_components


def monomers():
    Monomer('ERK', 's', 'state', {'state': ['up', 'p']})

    Parameter('ERK_0', 1e3)

    alias_model_components

    Initial(ERK(s=None, state='up'), ERK_0)


def by_BRAF_wt():

    Parameter('k_bwf', 1)
    Parameter('k_bwr', 0.1)
    Parameter('k_bwe', 1)

    alias_model_components()

    catalyze_state(BRAF(d=1, vem=None), 'erk', ERK(), 's',
                   'state', 'up', 'p', (k_bwf, k_bwr, k_bwe))


def by_BRAF_mut():

    Parameter('k_bmf', 1)
    Parameter('k_bmr', 0.1)
    Parameter('k_bme', 3)

    alias_model_components()

    catalyze_state(BRAF(vem=None), 'erk', ERK(), 's',
                   'state', 'up', 'p', (k_bmf, k_bmr, k_bme))


def by_CRAF():

    Parameter('k_cwf', 1)
    Parameter('k_cwr', 0.1)
    Parameter('k_cwe', 1)

    alias_model_components()

    catalyze_state(CRAF(d=1, vem=None), 'erk', ERK(), 's',
                   'state', 'up', 'p', (k_cwf, k_cwr, k_cwe))
