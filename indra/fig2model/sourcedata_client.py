import requests
import json

base_url = 'http://sourcedata.vital-it.ch/public/php/api/index.php'


def get_json(search_term, type='generic', limit=20, motif='scale'):
    params = {'limit': limit, 'motif': motif}
    search_url = base_url + '/%s/' % type + '%s' % search_term
    r = requests.get(search_url, params,
                     auth=('skartik', 'ivMnEFIelyov'))
    r.raise_for_status()
    dict = r.json()
    return dict


def save_json(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f)


        
def get_pmids(json):
    papers = {}
    for _, paper in enumerate(json['results']['direct']):
        paper_key = 'PMID' + paper['pmid']
        papers[paper_key] = get_hypos(paper)
        # h = hypotheses(paper)
        # papers[paper_key] = h.hypos
    return papers    


def get_hypos(paper):
    hypos = []
    for _, hypo in enumerate(paper['hypos']):
        ids = links(hypo)
        hypos.append({hypo['hypo']: ids.panels})
    return hypos    

class hypotheses:
    def __init__(self, paper):
        hypos = []
        for _, hypo in enumerate(paper['hypos']):
            ids = links(hypo)
            hypos.append({hypo['hypo']: ids.panels})
        self.hypos = hypos    

# def get_panel_ids(hypo):
#     ids = []
#     for _, panel in enumerate(hypo['panels']):
#         ids.append(panel['panel_id'])
#     return ids

class links:
    def __init__(self, hypo):
        ids = []
        for _, panel in enumerate(hypo['panels']):
            ids.append(panel['panel_id'])
        self.panels = ids
    
    


