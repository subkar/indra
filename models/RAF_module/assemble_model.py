import os
from pysb import *
import pysb.export
from indra import trips
from indra.assemblers import PysbAssembler
from enumerate_rules import enumerate_rules

def apply_patch(original, patch):
    orig_lines = [s.strip() for s in original.strip().split('\n')]
    patch_lines = [s.strip() for s in patch.strip().split('\n')]
    remove_lines = []
    add_lines = []
    for p in patch_lines:
        if p.startswith('<'):
            remove_lines.append(p[2:].strip())
        elif p.startswith('>'):
            add_lines.append(p[2:].strip())
    new_lines = []
    for o in orig_lines:
        if o not in remove_lines:
            new_lines.append(o)
    new_lines += add_lines
    new_txt = '\n'.join(new_lines)
    return new_txt

def assemble_model(model_id):
    print 'Reading model %d' % model_id
    model_name = 'model%d' % model_id
    # If model has already been read, just process the EKB XML
    if os.path.exists(model_name + '.xml'):
        tp = trips.process_xml(open(model_name + '.xml').read())
    else:
        # Start with the basic model
        model_txt = open('model1.txt').read()
        # Apply patches one by one to get to the current model text
        for j in range(1, model_id):
            patch_txt = open('model%d_from%d.txt' % (j+1, j)).read()
            model_txt = apply_patch(model_txt, patch_txt)
        print model_txt
        # Process model text and save result EKB XML
        tp = trips.process_text(model_txt, model_name + '.xml')

    # Assemble the PySB model
    pa = PysbAssembler()
    pa.add_statements(tp.statements)
    model = pa.make_model(policies='two_step')

    # Set initial conditions
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
    obs4 = Observable('BRAF_active', braf(vemurafenib=None))
    model.add_component(obs4)
    model.parameters['BRAF_0'].value = 0

    # Add mutated form of BRAF as initial condition
    sites_dict = {}
    for site in braf.sites:
        if site in braf.site_states:
            sites_dict[site] = braf.site_states[site][0]
        else:
            sites_dict[site] = None
    sites_dict['V600'] = 'E'
    model.add_component(Parameter('BRAF_mut_0', 1e5))
    model.initial(braf(**sites_dict), model.parameters['BRAF_mut_0'])

    # Set up model parameters
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

    model.parameters['kf_vb_bind_1'].value = 10
    model.parameters['kr_vb_bind_1'].value = 1

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

    if model_id >= 2:
        model.parameters['lrrc6_0'].value = 1e2
        model.parameters['kf_ms_bind_1'].value = 1e-05
        model.parameters['kr_ms_bind_1'].value = 1e-04
        model.parameters['kc_ms_phos_1'].value = 1
        model.parameters['kf_ls_bind_1'].value = 1
        model.parameters['kr_ls_bind_1'].value = 0.1
        model.parameters['kc_ls_dephos_1'].value = 1e-04

    if model_id >= 3:
        model.parameters['kf_bb_bind_1'].value = 10
        model.parameters['kr_bb_bind_1'].value = 1

    if model_id == 4:
        model.parameters['kf_vb_bind_2'].value = 1e-04

    pa.model = model
    pa.save_model('model%d.py' % model_id)
    return model
