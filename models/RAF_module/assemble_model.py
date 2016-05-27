import os
import sys
sys.path.append('../..')
from indra.assemblers import PysbAssembler
from indra import trips
import pysb.export
from pysb import *
from run_model import run_model

for i in range(3):
    tp = trips.process_text(open('model_%s.text' % (i+1)).read())
    pa = PysbAssembler()
    pa.add_statements(tp.statements)
    model = pa.make_model(policies='two_step')
    
    erk = model.monomers['MAPK1']
    obs = Observable('ERK_p', erk(phospho='p'))
    vem = model.monomers['VEMURAFENIB']
    obs2 = Observable('Vem_obs', vem(braf=None))
    ras = model.monomers['NRAS']
    obs3 = Observable('RAS_active', ras(gtp=ANY))
    model.add_component(obs)
    model.add_component(obs2)
    model.add_component(obs3)
    braf = model.monomers['BRAF']
    model.parameters['BRAF_0'].value = 0

    sites_dict = {}


    for site in braf.sites:
        if site in braf.site_states:
            sites_dict[site] = braf.site_states[site][0]
        else:
            sites_dict[site] = None
    sites_dict['V600'] = 'E'
    model.add_component(Parameter('BRAF_mut_0', 1e5))
    model.initial(braf(**sites_dict), model.parameters['BRAF_mut_0'])

    model.parameters['kf_ee_bind_1'].value = 1
    model.parameters['kr_ee_bind_1'].value = 0.1
    model.parameters['kf_ee_bind_2'].value = 1
    model.parameters['kr_ee_bind_2'].value = 0.1
    model.parameters['kf_eg_bind_1'].value = 1
    model.parameters['kr_eg_bind_1'].value = 0.1
    model.parameters['kf_gs_bind_1'].value = 1
    model.parameters['kr_gs_bind_1'].value = 0.1
    model.parameters['kf_sn_bind_1'].value = 1
    model.parameters['kr_sn_bind_1'].value = 50
    model.parameters['kf_ng_bind_1'].value = 50
    model.parameters['kr_ng_bind_1'].value = 0.5
    model.parameters['kf_nb_bind_1'].value = 1
    model.parameters['kr_nb_bind_1'].value = 0.5

    model.parameters['kf_vb_bind_1'].value = 0.1
    model.parameters['kr_vb_bind_1'].value = 0.1
    
    model.parameters['kf_bm_bind_1'].value = 1
    model.parameters['kr_bm_bind_1'].value = 0.1
    model.parameters['kc_bm_phos_1'].value = 3
    model.parameters['kf_pm_bind_1'].value = 1
    model.parameters['kr_pm_bind_1'].value = 0.001
    model.parameters['kc_pm_dephos_1'].value = 10
    model.parameters['kf_mm_bind_1'].value = 1
    model.parameters['kr_mm_bind_1'].value = 0.1
    model.parameters['kc_mm_phos_1'].value = 10
    model.parameters['kf_dm_bind_1'].value = 1
    model.parameters['kr_dm_bind_1'].value = 0.001
    model.parameters['kc_dm_dephos_1'].value = 10


    model.parameters['VEMURAFENIB_0'].value = 0
    model.parameters['EGF_0'].value = 1e3
    model.parameters['EGFR_0'].value = 1e5
    model.parameters['SOS1_0'].value = 1e3
    model.parameters['GRB2_0'].value = 1e5
    model.parameters['NRAS_0'].value = 2e5
    model.parameters['GTP_0'].value = 1e7
    model.parameters['MAP2K1_0'].value = 1e5
    model.parameters['MAPK1_0'].value = 1e5
    model.parameters['DUSP6_0'].value = 1e3
    model.parameters['PPP2CA_0'].value = 1e5
    

    feedback_params = ['PHOSPHATASE_0',
                       'kf_ms_bind_1', 'kr_ms_bind_1', 'kc_ms_phos_1',
                       'kf_ps_bind_1', 'kr_ps_bind_1', 'kc_ps_dephos_1']

    if set(feedback_params) < set([p.name for p in model.parameters]):
        print 'it matches'
        model.parameters['PHOSPHATASE_0'].value = 1e2
        model.parameters['kf_ms_bind_1'].value = 1e-04
        model.parameters['kr_ms_bind_1'].value = 1e-04
        model.parameters['kc_ms_phos_1'].value = 1
        model.parameters['kf_ps_bind_1'].value = 1
        model.parameters['kr_ps_bind_1'].value = 0.1
        model.parameters['kc_ps_dephos_1'].value = 1e-04
        

    braf_dimerization_params = ['kf_bb_bind_1', 'kr_bb_bind_1']
    
    if set(braf_dimerization_params) < set([p.name for p in model.parameters]):
        model.parameters['kf_bb_bind_1'].value = 1
        model.parameters['kr_bb_bind_1'].value = 1e-04   
 
    pa.save_model('model_%d.py' % (i+1))
    run_model(model, 'model_%d_plot.png' & (i+1))






    
