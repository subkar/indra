class Publication(object):
    def __init__(self, paper):
        self.pmid = paper['pmid']
        # self.hypotheses = [Hypothesis(h) for h in paper['hypos']]
    

    def __str__(self):
        return ("Publication PMID:" + self.pmid)

    
    def __repr__(self):
        return ("<pmid: %s, %d hypotheses at 0x%x>" %
                (self.pmid, len(self.hypotheses), id(self)))


    def hypotheses(self, paper, mlist):
        if not mlist:
            self.hypotheses = [Hypothesis(h) for h in paper['hypos']]
        elif mlist:
            hlist = []
            for h in paper['hypos']:
                hy = Hypothesis(h)
                if hy.assayed and hy.intervention in mlist:
                    hlist.append(hy)
            self.hypotheses = hlist

            
class Hypothesis(object):
    def __init__(self, hypothesis):
        self.assertion = hypothesis['hypo']
        self.assayed = hypothesis['displayRight'][0].lower()
        self.intervention = hypothesis['displayLeft'][0].lower()
        fig_base_url = 'http://sourcedata.vital-it.ch/public/#/panel/'
        self.panels = [fig_base_url + panel['panel_id']
                       for panel in hypothesis['panels']]
        

    def __repr__(self):
        return("<Assertion: %s, %d panels at 0x%x>" %
               (self.assertion, len(self.panels) , id(self)))




