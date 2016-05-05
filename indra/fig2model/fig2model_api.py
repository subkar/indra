import sourcedata_client as sdc
from process import Publication, Hypothesis

def process_query(query, save_json_name = 'sd_output.json'):
    dict = sdc.get_json(query)
    sdc.save_json(dict, save_json_name)
    return process_json(dict)


def process_json(dict):
    papers = []
    for paper in dict['results']['direct']:
        if paper['pmid'] != None:
            papers.append(Publication(paper))
    return papers


