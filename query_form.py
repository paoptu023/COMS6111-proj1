class query_form(object):
    """docstring for ClassName"""

    def __init__(self, query):
        self.relevant_set = {}
        self.non_relevant_set = {}
        self.query = query
        self.Dr = 0
        self.Dnr = 0
        self.alpha = 1
        self.beta = 1
        self.gamma = 1

    def add_relevant_doc(self, doc):
        self.relevant_set.add(doc)
        self.Dr += 1

    def add_non_relevant_doc(self, doc):
        self.non_relevant_set.add(doc)
        self.Dnr += 1

    def form_query(self):
        new_query = []
        return new_query

    def get_precision(self):
        return self.Dr/10.0
