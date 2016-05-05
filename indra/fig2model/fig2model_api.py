import sourcedata_client as sdc
from process import Publication, Hypothesis

def process_query(query, mlist=[], save_json_name = 'sd_output.json'):
    dict = sdc.get_json(query, limit=100)
    sdc.save_json(dict, save_json_name)
    return process_json(dict, mlist)


def process_json(dict, mlist):
    papers = []
    for paper in dict['results']['direct']:
        if paper['pmid'] != None:
            p = Publication(paper)
            p.hypotheses(paper, mlist)
            papers.append(p)            
    return papers


