import requests
import xml.etree.ElementTree as ET
import re
from indra import reach
import json
from process_captions import Refs

base_url = "http://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"

def get_xml(pmcid):

    params = {'verb': 'GetRecord',
              'identifier': "oai:pubmedcentral.nih.gov:%s" % pmcid,
              'metadataPrefix': 'pmc'}
    r = requests.get(base_url, params)
    r.raise_for_status()
    xml = r.text
    return xml

def parse_xml(pmcid):
    xml = get_xml(pmcid)
    xml = xml.encode('utf-8')
    tree = ET.fromstring(xml)
    try:
        tree[2].attrib['code'] == 'cannotDisseminateFormat'
        captions = 'XML not available'
    except KeyError:
        captions = get_captions(xml)
    return captions


def get_captions(xml):
    tree = ET.fromstring(xml)
    captions = []
    metadata = tree.findall('.//{http://www.openarchives.org/OAI/2.0/}metadata')
    tag = metadata[0][0].tag
    schema_location = re.split('\}', tag)[0] + '}'
    caption_tag = schema_location + 'caption'

    for caption in tree.findall(
            './/' + caption_tag):
        p = caption.find(schema_location + 'p')
        if p is not None:
            text = ''.join([i for i in p.itertext()])
            captions.append(text)
    return captions        


def process_caption(caption):
    rp = reach.process_text(caption, offline=True)
    json_output = open('reach_output.json').read()
    js = json.loads(json_output)
    entities = []
    for entity in js['entities']['frames']:
        entities.append(Refs(entity))
    return entities                    
                

    

    
