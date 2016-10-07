import math
import operator
import parameters

class processor(object):
    """
    This class is mainly to process the retrieved documents to improve the query
    """

    def __init__(self, query):
        self.relevant_set = []
        self.non_relevant_set = []
        self.query = query

    def add_relevant_doc(self, doc):
        self.relevant_set.append(doc)

    def add_non_relevant_doc(self, doc):
        self.non_relevant_set.append(doc)

    def cal_freq(self, docs, tf):
        for doc in docs:
            for term in doc:
                if term in tf:
                    tf[term] += 1
                else:
                    tf[term] = 1
        return tf

    def form_query(self):
        vectors = {}  # document vectors
        tf_r = {}  # term frequency of relevant docs
        tf_nr = {}  # term frequency of non relevant docs
        df = {}  # document frequency
        Dr = len(self.relevant_set)  # number of relevant docs
        Dnr = len(self.non_relevant_set)  # number of non relevant docs

        # parse documents
        docs_r = parameters.param.parser(self.relevant_set)
        docs_nr = parameters.param.parser(self.non_relevant_set)

        # count the frequency of each term in docs
        self.cal_freq(docs_r, tf_r)
        self.cal_freq(docs_nr, tf_nr)

        # count the document frequency
        for doc in docs_r+docs_nr:
            for term in set(doc):
                if term in df:
                    df[term] += 1
                else:
                    df[term] = 1
                    vectors[term] = 0.0

        # calculate weights
        for (term, freq) in self.query.items():
            vectors[term] = (parameters.param.alpha * freq)

        for term in tf_r:
            vectors[term] += parameters.param.beta *float(tf_r[term])*math.log(float(parameters.param.num)/(df[term]))/Dr

        for term in tf_nr:
            vectors[term] -= parameters.param.gamma * float(tf_nr[term])*math.log(float(parameters.param.num)/(df[term]))/Dnr

        # compose new query
        q = {key: vectors[key] for key in vectors if vectors[key] > 0}
        new_q = sorted(q.items(), key=operator.itemgetter(1), reverse=True)

        cnt = 0
        for (term, freq) in new_q:
            if term in self.query:
                self.query[term] += freq
            elif term not in self.query and len(term)<10 and cnt<parameters.param.add_terms:
                self.query[term] = freq
                cnt += 1

        reorder_q = sorted(self.query.items(), key=operator.itemgetter(1), reverse=True)
        self.query = {term: score for (term, score) in reorder_q}
        return self.query