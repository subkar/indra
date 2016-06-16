import sourcedata_client as sdc
from process import Publication, Hypothesis
from process2 import Panel

def process_query(query, save_json_name = 'sd_output.json'):
    dict = sdc.get_json(query, limit=100)
    sdc.save_json(dict, save_json_name)
    return process_ids(get_panelids(dict))


def get_panelids(dict):
    panel_ids = []
    for paper in dict['results']['direct']:
        for panel in paper['hypos'][0]['panels']:
            panel_ids.append(panel['panel_id'])

    return panel_ids


def process_ids(panel_ids):
    assert type(panel_ids) == list
    panels = []
    for id in panel_ids:
        panel_dict = sdc.get_panel_info(id)
        pmid = sdc.get_pmids(panel_dict)
        p = Panel(panel_dict, pmid)
        p.figure_label(panel_dict)
        p.caption(panel_dict)
        p.href(panel_dict)
        p.assay(panel_dict)
        panels.append(p)

    return panels
