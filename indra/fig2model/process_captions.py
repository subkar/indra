class Refs(object):
    def __init__(self, entity):
        self.refs = {'type': entity['type'],
                     entity['xrefs'][0]['namespace']:
                     entity['xrefs'][0]['id']}
        self.name = entity['text']


    def __str__(self):
        return self.name


    def __repr__(self):
        return ("<%s at 0x%x>" % (self.name, id(self)))
