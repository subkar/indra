import requests
import json

for line in open('authentication.txt'):
    key = tuple(line.strip().split(':'))

base_url = 'http://sourcedata.vital-it.ch/public/php/api/index.php'


def get_json(search_term, type='generic', limit=20, motif='scale'):
    params = {'limit': limit, 'motif': motif}
    search_url = base_url + '/%s/' % type + '%s' % search_term
    r = requests.get(search_url, params, auth=key)
    r.raise_for_status()
    dict = r.json()
    return dict


def save_json(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f)


        
