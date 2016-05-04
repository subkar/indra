
def get_pmids(json):
    papers = {}
    for _, paper in enumerate(json['results']['direct']):
        paper_key = 'PMID' + paper['pmid']
        papers[paper_key] = get_hypos(paper)
    return papers

    
def get_hypos(paper):
    hypos = []
    for _, hypo in enumerate(paper['hypos']):
        ids = get_panel_ids(hypo)
        hypos.append({hypo['hypo']: ids})
    return hypos    


def get_panel_ids(hypo):
    ids = []
    for _, panel in enumerate(hypo['panels']):
        ids.append(panel['panel_id'])
    return ids

# class links:
#     def __init__(self, hypo):
#         ids = []
#         for _, panel in enumerate(hypo['panels']):
#             ids.append(panel['panel_id'])
#         self.panels = ids



