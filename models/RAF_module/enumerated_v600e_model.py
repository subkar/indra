# exported from PySB model 'None'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, Annotation, ANY, WILD

Model()

Monomer('VEMURAFENIB', ['braf'])
Monomer('SOS1', ['phospho', 'grb2', 'nras', 'mapk1', 'lrrc6'], {'phospho': ['u', 'p']})
Monomer('PPP2CA', ['map2k1'])
Monomer('EGFR', ['egf', 'egfr', 'grb2'])
Monomer('lrrc6', ['sos1'])
Monomer('NRAS', ['braf', 'sos1', 'gtp'])
Monomer('GTP', ['nras'])
Monomer('MAP2K1', ['phospho', 'braf', 'mapk1', 'ppp2ca'], {'phospho': ['u', 'p']})
Monomer('GRB2', ['egfr', 'sos1'])
Monomer('BRAF', ['nras', 'V600', 'braf', 'vemurafenib', 'map2k1'], {'V600': ['WT', 'E']})
Monomer('MAPK1', ['map2k1', 'phospho', 'sos1', 'dusp6'], {'phospho': ['u', 'p']})
Monomer('DUSP6', ['mapk1'])
Monomer('EGF', ['egfr'])

Parameter('kf_ee_bind_1', 1)
Parameter('kr_ee_bind_1', 1e-01)
Parameter('kf_ee_bind_2', 1)
Parameter('kr_ee_bind_2', 1e-01)
Parameter('kf_eg_bind_1', 1)
Parameter('kr_eg_bind_1', 1e-01)
Parameter('kf_gs_bind_1', 1)
Parameter('kr_gs_bind_1', 1e-01)
Parameter('kf_nb_bind_1', 1)
Parameter('kr_nb_bind_1', 0.5)

Parameter('kf_sn_bind_1', 1)
Parameter('kr_sn_bind_1', 50)
Parameter('kf_ng_bind_1', 50)
Parameter('kr_ng_bind_1', 0.5)

Parameter('kf_bb_bind_1_nA_vA_nA_vA', 1e-02)
Parameter('kr_bb_bind_1_nA_vA_nA_vA', 1)
Parameter('kf_vb_bind_1_bA', 1e-02)
Parameter('kr_vb_bind_1_bA', 1e-01)
Parameter('kf_vb_bind_1_bA2', 1e-05)  # Manually added parameter
Parameter('kr_vb_bind_1_bA2', 1)  # Manually added parameter
Parameter('kf_vb_bind_1_bN', 1e-01)
Parameter('kr_vb_bind_1_bN', 1e-01)

Parameter('kf_bm_bind_1', 1)
Parameter('kr_bm_bind_1', 0.1)
Parameter('kc_bm_phos_1', 3)
Parameter('kf_pm_bind_1', 1)
Parameter('kr_pm_bind_1', 0.001)
Parameter('kc_pm_dephos_1', 10)
Parameter('kf_mm_bind_1', 1)
Parameter('kr_mm_bind_1', 0.1)
Parameter('kc_mm_phos_1', 10)
Parameter('kf_dm_bind_1', 1)
Parameter('kr_dm_bind_1', 0.001)
Parameter('kc_dm_dephos_1', 10)
Parameter('kf_ms_bind_1', 1e-04)
Parameter('kr_ms_bind_1', 1e-04)
Parameter('kc_ms_phos_1', 1)
Parameter('kf_ls_bind_1', 1)
Parameter('kr_ls_bind_1', 0.1)
Parameter('kc_ls_dephos_1', 1e-04)
Parameter('VEMURAFENIB_0', 0)
Parameter('SOS1_0', 1e3)
Parameter('PPP2CA_0', 1e5)
Parameter('EGFR_0', 1e5)
Parameter('lrrc6_0', 100.0)
Parameter('NRAS_0', 2e5)
Parameter('GTP_0', 1e7)
Parameter('MAP2K1_0', 1e5)
Parameter('GRB2_0', 1e5)
Parameter('BRAF_0', 1e5)
Parameter('MAPK1_0', 1e5)
Parameter('DUSP6_0', 1e3)
Parameter('EGF_0', 1e3)

Parameter('kf_bb_bind_1_nN_vN_nN_vN', 1e-06) # 1e-06
Parameter('kf_bb_bind_1_nN_vN_nN_vA', 1e-03) # 1e-03
Parameter('kf_bb_bind_1_nN_vN_nA_vN', 0) # 0
Parameter('kf_bb_bind_1_nN_vN_nA_vA', 0) # 0
Parameter('kf_bb_bind_1_nN_vA_nN_vA', 1e-08) # 1e-08
Parameter('kf_bb_bind_1_nN_vA_nA_vN', 0) # 0
Parameter('kf_bb_bind_1_nN_vA_nA_vA', 0) # 0
Parameter('kf_bb_bind_1_nA_vN_nA_vN', 1) # 1
Parameter('kf_bb_bind_1_nA_vN_nA_vA', 1) # 1
Parameter('kr_bb_bind_1_nN_vN_nN_vN', 1) # 1
Parameter('kr_bb_bind_1_nN_vN_nN_vA', 1) # 1
Parameter('kr_bb_bind_1_nN_vN_nA_vN', 0) # 0
Parameter('kr_bb_bind_1_nN_vN_nA_vA', 0) # 0
Parameter('kr_bb_bind_1_nN_vA_nN_vA', 1) # 1
Parameter('kr_bb_bind_1_nN_vA_nA_vN', 0) # 0
Parameter('kr_bb_bind_1_nN_vA_nA_vA', 0) # 0
Parameter('kr_bb_bind_1_nA_vN_nA_vN', 1e-04) # 1e-04
Parameter('kr_bb_bind_1_nA_vN_nA_vA', 1e-04) # 1e-04


# EGF to RAS
# ---------
Rule('EGFR_EGF_bind',
     EGFR(egf=None) + EGF(egfr=None) >> 
     EGFR(egf=1) % EGF(egfr=1),
     kf_ee_bind_1)
Rule('EGFR_EGF_dissociate',
     EGFR(egf=1) % EGF(egfr=1) >> 
     EGFR(egf=None) + EGF(egfr=None),
     kr_ee_bind_1)
Rule('EGFR_EGF_EGFR_EGF_bind',
     EGFR(egf=ANY, egfr=None) + EGFR(egf=ANY, egfr=None) >> 
     EGFR(egf=ANY, egfr=1) % EGFR(egf=ANY, egfr=1),
     kf_ee_bind_2)
Rule('EGFR_EGFR_dissociate',
     EGFR(egfr=1) % EGFR(egfr=1) >> 
     EGFR(egfr=None) + EGFR(egfr=None),
     kr_ee_bind_2)
Rule('EGFR_EGFR_GRB2_bind',
     EGFR(egfr=ANY, grb2=None) + GRB2(egfr=None) >> 
     EGFR(egfr=ANY, grb2=1) % GRB2(egfr=1),
     kf_eg_bind_1)
Rule('EGFR_GRB2_dissociate',
     EGFR(grb2=1) % GRB2(egfr=1) >> 
     EGFR(grb2=None) + GRB2(egfr=None),
     kr_eg_bind_1)
Rule('GRB2_EGFR_SOS1_phospho_bind',
     GRB2(egfr=ANY, sos1=None) + SOS1(phospho='u', grb2=None) >> 
     GRB2(egfr=ANY, sos1=1) % SOS1(phospho='u', grb2=1),
     kf_gs_bind_1)
Rule('GRB2_SOS1_dissociate',
     GRB2(sos1=1) % SOS1(grb2=1) >> 
     GRB2(sos1=None) + SOS1(grb2=None),
     kr_gs_bind_1)
Rule('SOS1_phospho_GRB2_NRAS_nBRAF_bind',
     SOS1(phospho='u', grb2=ANY, nras=None) + NRAS(braf=None, sos1=None) >> 
     SOS1(phospho='u', grb2=ANY, nras=1) % NRAS(braf=None, sos1=1),
     kf_sn_bind_1)
Rule('SOS1_NRAS_dissociate',
     SOS1(nras=1) % NRAS(sos1=1) >> 
     SOS1(nras=None) + NRAS(sos1=None),
     kr_sn_bind_1)
Rule('NRAS_SOS1_GTP_bind',
     NRAS(sos1=ANY, gtp=None) + GTP(nras=None) >> 
     NRAS(sos1=ANY, gtp=1) % GTP(nras=1),
     kf_ng_bind_1)
Rule('NRAS_GTP_dissociate',
     NRAS(gtp=1) % GTP(nras=1) >> 
     NRAS(gtp=None) + GTP(nras=None),
     kr_ng_bind_1)

# BRAF dynamics
# -------------

Rule('NRAS_GTP_nSOS1_BRAF_V600E_bind',
     NRAS(braf=None, sos1=None, gtp=ANY) + BRAF(nras=None, V600='E') >> 
     NRAS(braf=1, sos1=None, gtp=ANY) % BRAF(nras=1, V600='E'),
     kf_nb_bind_1)
Rule('NRAS_BRAF_V600E_dissociate',
     NRAS(braf=1) % BRAF(nras=1, V600='E') >> 
     NRAS(braf=None) + BRAF(nras=None, V600='E'),
     kr_nb_bind_1)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasA_vemurafenibA_nrasA_vemurafenibA',
     BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY) >> 
     BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY),
     kf_bb_bind_1_nA_vA_nA_vA)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasA_vemurafenibA_nrasA_vemurafenibA',
     BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY) >> 
     BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY),
     kr_bb_bind_1_nA_vA_nA_vA)

# Manually modified rules
# ----------------------
Rule('VEMURAFENIB_BRAF_V600E_bind_brafA',
     VEMURAFENIB(braf=None) +
     BRAF(V600='E', braf=2, vemurafenib=None) % BRAF(V600='E', braf=2, vemurafenib=None) >> 
     VEMURAFENIB(braf=1) % BRAF(V600='E', braf=2, vemurafenib=1) % BRAF(V600='E', braf=2, vemurafenib=None),
     kf_vb_bind_1_bA)
Rule('VEMURAFENIB_BRAF_V600E_dissociate_brafA',
     VEMURAFENIB(braf=1) %
     BRAF(V600='E', braf=2, vemurafenib=1) % BRAF(V600='E', braf=2, vemurafenib=None) >> 
     VEMURAFENIB(braf=None) + BRAF(V600='E', braf=2, vemurafenib=None) % BRAF(V600='E', braf=2, vemurafenib=None),
     kr_vb_bind_1_bA)

Rule('VEMURAFENIB_BRAF_V600E_bind_brafA2',
     VEMURAFENIB(braf=None) +
     BRAF(V600='E', braf=2, vemurafenib=None) % BRAF(V600='E', braf=2, vemurafenib=ANY) >> 
     VEMURAFENIB(braf=1) % BRAF(V600='E', braf=2, vemurafenib=1) % BRAF(V600='E', braf=2, vemurafenib=ANY),
     kf_vb_bind_1_bA2)
Rule('VEMURAFENIB_BRAF_V600E_dissociate_brafA2',
     VEMURAFENIB(braf=1) %
     BRAF(V600='E', braf=2, vemurafenib=1) % BRAF(V600='E', braf=2, vemurafenib=ANY) >> 
     VEMURAFENIB(braf=None) + BRAF(V600='E', braf=2, vemurafenib=None) % BRAF(V600='E', braf=2, vemurafenib=ANY),
     kr_vb_bind_1_bA2)

# BRAF to ERK
# -----------
Rule('BRAF_V600E_nVEMURAFENIB_phospho_bind_MAP2K1_phospho_1',
     BRAF(V600='E', vemurafenib=None, map2k1=None) + MAP2K1(phospho='u', braf=None) >> 
     BRAF(V600='E', vemurafenib=None, map2k1=1) % MAP2K1(phospho='u', braf=1),
     kf_bm_bind_1)
Rule('BRAF_V600E_nVEMURAFENIB_phospho_MAP2K1_phospho_1',
     BRAF(V600='E', vemurafenib=None, map2k1=1) % MAP2K1(phospho='u', braf=1) >> 
     BRAF(V600='E', vemurafenib=None, map2k1=None) + MAP2K1(phospho='p', braf=None),
     kc_bm_phos_1)
Rule('BRAF_V600E_dissoc_MAP2K1',
     BRAF(V600='E', map2k1=1) % MAP2K1(braf=1) >> 
     BRAF(V600='E', map2k1=None) + MAP2K1(braf=None),
     kr_bm_bind_1)
Rule('PPP2CA_dephos_bind_MAP2K1_nMAPK1_phospho_1',
     PPP2CA(map2k1=None) + MAP2K1(phospho='p', mapk1=None, ppp2ca=None) >> 
     PPP2CA(map2k1=1) % MAP2K1(phospho='p', mapk1=None, ppp2ca=1),
     kf_pm_bind_1)
Rule('PPP2CA_dephos_MAP2K1_nMAPK1_phospho_1',
     PPP2CA(map2k1=1) % MAP2K1(phospho='p', mapk1=None, ppp2ca=1) >> 
     PPP2CA(map2k1=None) + MAP2K1(phospho='u', mapk1=None, ppp2ca=None),
     kc_pm_dephos_1)
Rule('PPP2CA_dissoc_MAP2K1',
     PPP2CA(map2k1=1) % MAP2K1(ppp2ca=1) >> 
     PPP2CA(map2k1=None) + MAP2K1(ppp2ca=None),
     kr_pm_bind_1)
Rule('MAP2K1_nPPP2CA_phospho_bind_MAPK1_phospho_1',
     MAP2K1(phospho='p', mapk1=None, ppp2ca=None) + MAPK1(map2k1=None, phospho='u') >> 
     MAP2K1(phospho='p', mapk1=1, ppp2ca=None) % MAPK1(map2k1=1, phospho='u'),
     kf_mm_bind_1)
Rule('MAP2K1_nPPP2CA_phospho_MAPK1_phospho_1',
     MAP2K1(phospho='p', mapk1=1, ppp2ca=None) % MAPK1(map2k1=1, phospho='u') >> 
     MAP2K1(phospho='p', mapk1=None, ppp2ca=None) + MAPK1(map2k1=None, phospho='p'),
     kc_mm_phos_1)
Rule('MAP2K1_dissoc_MAPK1',
     MAP2K1(mapk1=1) % MAPK1(map2k1=1) >> 
     MAP2K1(mapk1=None) + MAPK1(map2k1=None),
     kr_mm_bind_1)
Rule('DUSP6_dephos_bind_MAPK1_nSOS1_phospho_1',
     DUSP6(mapk1=None) + MAPK1(phospho='p', sos1=None, dusp6=None) >> 
     DUSP6(mapk1=1) % MAPK1(phospho='p', sos1=None, dusp6=1),
     kf_dm_bind_1)
Rule('DUSP6_dephos_MAPK1_nSOS1_phospho_1',
     DUSP6(mapk1=1) % MAPK1(phospho='p', sos1=None, dusp6=1) >> 
     DUSP6(mapk1=None) + MAPK1(phospho='u', sos1=None, dusp6=None),
     kc_dm_dephos_1)
Rule('DUSP6_dissoc_MAPK1',
     DUSP6(mapk1=1) % MAPK1(dusp6=1) >> 
     DUSP6(mapk1=None) + MAPK1(dusp6=None),
     kr_dm_bind_1)
Rule('MAPK1_nDUSP6_phospho_bind_SOS1_nNRAS_phospho_1',
     MAPK1(phospho='p', sos1=None, dusp6=None) + SOS1(phospho='u', nras=None, mapk1=None) >> 
     MAPK1(phospho='p', sos1=1, dusp6=None) % SOS1(phospho='u', nras=None, mapk1=1),
     kf_ms_bind_1)
Rule('MAPK1_nDUSP6_phospho_SOS1_nNRAS_phospho_1',
     MAPK1(phospho='p', sos1=1, dusp6=None) % SOS1(phospho='u', nras=None, mapk1=1) >> 
     MAPK1(phospho='p', sos1=None, dusp6=None) + SOS1(phospho='p', nras=None, mapk1=None),
     kc_ms_phos_1)
Rule('MAPK1_dissoc_SOS1',
     MAPK1(sos1=1) % SOS1(mapk1=1) >> 
     MAPK1(sos1=None) + SOS1(mapk1=None),
     kr_ms_bind_1)
Rule('lrrc6_dephos_bind_SOS1_phospho_1',
     lrrc6(sos1=None) + SOS1(phospho='p', lrrc6=None) >> 
     lrrc6(sos1=1) % SOS1(phospho='p', lrrc6=1),
     kf_ls_bind_1)
Rule('lrrc6_dephos_SOS1_phospho_1',
     lrrc6(sos1=1) % SOS1(phospho='p', lrrc6=1) >> 
     lrrc6(sos1=None) + SOS1(phospho='u', lrrc6=None),
     kc_ls_dephos_1)
Rule('lrrc6_dissoc_SOS1', lrrc6(sos1=1) % SOS1(lrrc6=1) >> 
     lrrc6(sos1=None) + SOS1(lrrc6=None),
     kr_ls_bind_1)

# Enumerated rules
# ---------------
Rule('BRAF_V600E_BRAF_V600E_bind_nrasN_vemurafenibN_nrasN_vemurafenibN',
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=None, V600='E', braf=None, vemurafenib=None) >> 
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=None, V600='E', braf=1, vemurafenib=None),
     kf_bb_bind_1_nN_vN_nN_vN)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasN_vemurafenibN_nrasN_vemurafenibA',
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY),
     kf_bb_bind_1_nN_vN_nN_vA)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasN_vemurafenibN_nrasA_vemurafenibN',
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None) >> 
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None),
     kf_bb_bind_1_nN_vN_nA_vN)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasN_vemurafenibN_nrasA_vemurafenibA',
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY),
     kf_bb_bind_1_nN_vN_nA_vA)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasN_vemurafenibA_nrasN_vemurafenibA',
     BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY),
     kf_bb_bind_1_nN_vA_nN_vA)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasN_vemurafenibA_nrasA_vemurafenibN',
     BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None) >> 
     BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None),
     kf_bb_bind_1_nN_vA_nA_vN)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasN_vemurafenibA_nrasA_vemurafenibA',
     BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY),
     kf_bb_bind_1_nN_vA_nA_vA)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasA_vemurafenibN_nrasA_vemurafenibN',
     BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None) >> 
     BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None),
     kf_bb_bind_1_nA_vN_nA_vN)
Rule('BRAF_V600E_BRAF_V600E_bind_nrasA_vemurafenibN_nrasA_vemurafenibA',
     BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY) >> 
     BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY),
     kf_bb_bind_1_nA_vN_nA_vA)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasN_vemurafenibN_nrasN_vemurafenibN',
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=None, V600='E', braf=1, vemurafenib=None) >> 
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=None, V600='E', braf=None, vemurafenib=None),
     kr_bb_bind_1_nN_vN_nN_vN)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasN_vemurafenibN_nrasN_vemurafenibA',
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY),
     kr_bb_bind_1_nN_vN_nN_vA)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasN_vemurafenibN_nrasA_vemurafenibN',
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None) >> 
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None),
     kr_bb_bind_1_nN_vN_nA_vN)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasN_vemurafenibN_nrasA_vemurafenibA',
     BRAF(nras=None, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY),
     kr_bb_bind_1_nN_vN_nA_vA)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasN_vemurafenibA_nrasN_vemurafenibA',
     BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY),
     kr_bb_bind_1_nN_vA_nN_vA)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasN_vemurafenibA_nrasA_vemurafenibN',
     BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None) >> 
     BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None),
     kr_bb_bind_1_nN_vA_nA_vN)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasN_vemurafenibA_nrasA_vemurafenibA',
     BRAF(nras=None, V600='E', braf=1, vemurafenib=ANY) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY) >> 
     BRAF(nras=None, V600='E', braf=None, vemurafenib=ANY) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY),
     kr_bb_bind_1_nN_vA_nA_vA)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasA_vemurafenibN_nrasA_vemurafenibN',
     BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None) >> 
     BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None),
     kr_bb_bind_1_nA_vN_nA_vN)
Rule('BRAF_V600E_BRAF_V600E_dissociate_nrasA_vemurafenibN_nrasA_vemurafenibA',
     BRAF(nras=ANY, V600='E', braf=1, vemurafenib=None) % BRAF(nras=ANY, V600='E', braf=1, vemurafenib=ANY) >> 
     BRAF(nras=ANY, V600='E', braf=None, vemurafenib=None) + BRAF(nras=ANY, V600='E', braf=None, vemurafenib=ANY),
     kr_bb_bind_1_nA_vN_nA_vA)
Rule('VEMURAFENIB_BRAF_V600E_bind_brafN',
     VEMURAFENIB(braf=None) + BRAF(V600='E', braf=None, vemurafenib=None) >> 
     VEMURAFENIB(braf=1) % BRAF(V600='E', braf=None, vemurafenib=1),
     kf_vb_bind_1_bN)
Rule('VEMURAFENIB_BRAF_V600E_dissociate_brafN',
     VEMURAFENIB(braf=1) % BRAF(V600='E', braf=None, vemurafenib=1) >> 
     VEMURAFENIB(braf=None) + BRAF(V600='E', braf=None, vemurafenib=None),
     kr_vb_bind_1_bN)

Initial(VEMURAFENIB(braf=None), VEMURAFENIB_0)
Initial(SOS1(phospho='u', grb2=None, nras=None, mapk1=None, lrrc6=None), SOS1_0)
Initial(PPP2CA(map2k1=None), PPP2CA_0)
Initial(EGFR(egf=None, egfr=None, grb2=None), EGFR_0)
Initial(lrrc6(sos1=None), lrrc6_0)
Initial(NRAS(braf=None, sos1=None, gtp=None), NRAS_0)
Initial(GTP(nras=None), GTP_0)
Initial(MAP2K1(phospho='u', braf=None, mapk1=None, ppp2ca=None), MAP2K1_0)
Initial(GRB2(egfr=None, sos1=None), GRB2_0)
Initial(BRAF(nras=None, V600='E', braf=None, vemurafenib=None, map2k1=None), BRAF_0)
Initial(MAPK1(map2k1=None, phospho='u', sos1=None, dusp6=None), MAPK1_0)
Initial(DUSP6(mapk1=None), DUSP6_0)
Initial(EGF(egfr=None), EGF_0)

Annotation(VEMURAFENIB, 'http://identifiers.org/chebi/CHEBI:63637', 'is')
Annotation(SOS1, 'http://identifiers.org/pfam/PF00617', 'is')
Annotation(SOS1, 'http://identifiers.org/uniprot/Q62245', 'is')
Annotation(SOS1, 'http://identifiers.org/hgnc/HGNC:11187', 'is')
Annotation(PPP2CA, 'http://identifiers.org/pfam/PF00149', 'is')
Annotation(PPP2CA, 'http://identifiers.org/uniprot/P63330', 'is')
Annotation(PPP2CA, 'http://identifiers.org/hgnc/HGNC:9299', 'is')
Annotation(EGFR, 'http://identifiers.org/pfam/PF01030', 'is')
Annotation(EGFR, 'http://identifiers.org/uniprot/P0CY46', 'is')
Annotation(EGFR, 'http://identifiers.org/hgnc/HGNC:3236', 'is')
Annotation(lrrc6, 'http://identifiers.org/pfam/PF00328.17', 'is')
Annotation(lrrc6, 'http://identifiers.org/uniprot/Q9NJE9', 'is')
Annotation(NRAS, 'http://identifiers.org/uniprot/P01111', 'is')
Annotation(NRAS, 'http://identifiers.org/hgnc/HGNC:7989', 'is')
Annotation(GTP, 'http://identifiers.org/chebi/CHEBI:37565', 'is')
Annotation(MAP2K1, 'http://identifiers.org/uniprot/Q02750', 'is')
Annotation(MAP2K1, 'http://identifiers.org/hgnc/HGNC:6840', 'is')
Annotation(GRB2, 'http://identifiers.org/uniprot/P62993', 'is')
Annotation(GRB2, 'http://identifiers.org/hgnc/HGNC:4566', 'is')
Annotation(BRAF, 'http://identifiers.org/uniprot/P15056', 'is')
Annotation(BRAF, 'http://identifiers.org/hgnc/HGNC:1097', 'is')
Annotation(MAPK1, 'http://identifiers.org/pfam/PF00069', 'is')
Annotation(MAPK1, 'http://identifiers.org/uniprot/P63085', 'is')
Annotation(MAPK1, 'http://identifiers.org/hgnc/HGNC:6871', 'is')
Annotation(DUSP6, 'http://identifiers.org/uniprot/Q16828', 'is')
Annotation(DUSP6, 'http://identifiers.org/hgnc/HGNC:3072', 'is')
Annotation(EGF, 'http://identifiers.org/pfam/PF00008', 'is')
Annotation(EGF, 'http://identifiers.org/uniprot/P01132', 'is')
Annotation(EGF, 'http://identifiers.org/hgnc/HGNC:3229', 'is')


Observable('MAPK1_P', MAPK1(phospho='p'))
Observable('MAP2K1_P', MAP2K1(phospho='p'))
Observable('Vem_obs', VEMURAFENIB(braf=None))

