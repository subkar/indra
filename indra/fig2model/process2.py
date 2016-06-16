class Panel(object):
    def __init__(self, panel, pmid):
        self.pmid = pmid


    def figure_label(self, panel):
        for p in panel['figure']['panels']:
            if p['panel_id'] == panel['current_panel_id']:
                self.figure_label =  p['label']            

                
    def __str__(self):
        return ("Publication PMID:" + self.pmid)

    
    def __repr__(self):
        return ("<%s in  PMID%s at 0x%x>" %
                (self.figure_label, self.pmid, id(self)))


    def caption(self, panel):
        for p in panel['figure']['panels']:
            if p['panel_id'] == panel['current_panel_id']:
                self.caption = p['formatted_caption']


    def href(self, panel):
        for p in panel['figure']['panels']:
            if p['panel_id'] == panel['current_panel_id']:
                self.href = p['href']


    def assay(self, panel):
        for p in panel['figure']['panels']:
            if p['panel_id'] == panel['current_panel_id']:
                tags = p['tags']
        for tag in tags:
            if tag['category'] == 'assay':
                self.assay = tag['text']




