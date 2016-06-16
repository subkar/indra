import requests
import json
import os
PATH = os.path.dirname(__file__)
for line in open(os.path.join(PATH, 'authentication.txt')):
    key = tuple(line.strip().split(':'))

base_url = 'http://sourcedata.vital-it.ch/public/php/api/index.php'

def get_json(agents, limit = 20, motif = 'scale'):
    params = {'limit': limit,
     'motif': motif}
    search_url = base_url + '/intervention/%s/assayed/%s' % (agents[0], agents[1])
    r = requests.get(search_url, params, auth=key)
    r.raise_for_status()
    dict = r.json()
    return dict


def get_panel_info(panel_id):
    search_url = base_url + '/panel/%s' % panel_id
    r = requests.get(search_url, auth=key)
    r.raise_for_status()
    panel_dict = r.json()
    return panel_dict


def get_pmids(panel_dict):
    search_url = base_url + '/paper/%s' % panel_dict['paper']['doi']
    r = requests.get(search_url, auth=key)
    r.raise_for_status()
    pub_dict = r.json()
    return pub_dict['pmid']


def save_json(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f)
