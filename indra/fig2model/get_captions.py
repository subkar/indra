import requests
import xml.etree.ElementTree as ET

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
    for caption in tree.findall(
            './/{http://jats.nlm.nih.gov/ns/archiving/1.0/}caption'):
        p = caption.find('{http://jats.nlm.nih.gov/ns/archiving/1.0/}p')
        if p is not None:
            text = ''.join([i for i in p.itertext()])
            captions.append(text)
    return captions        
            
                

    

    
