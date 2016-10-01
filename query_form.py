import math
import pprint
import operator

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
        vectors = []
        df = {}
        total_tf = {}
        N = 10
        docs = []

        docs = self.relevant_set.union(self.non_relevant_set)

        # count the frequency of each term
        for d in docs:
            doc = d.split()
            tf = {}
            cnt = 1;
            if d in self.non_relevant_set:
                cnt = -1;

            for term in doc:
                if term in tf:
                    tf[term] += cnt
                else:
                    tf[term] = cnt
                if term in total_tf:
                    total_tf[term] += 1
                else:
                    total_tf[term] = 1
            vectors.append(tf)

        print 'term frequency : '
        pprint.pprint(vectors)
        print ''
        # calculate tf_ij and idf
        for vector in vectors:
            for (k, v) in vector.items():
                vector[k] = float(vector[k]) / total_tf[k]
                if k in df:
                    df[k] += 1
                else:
                    df[k] = 1

        print 'normalized term frequency :'
        pprint.pprint(vectors)
        print ''
        # calculate w_ij
        for vector in vectors:
            for (k, v) in vector.items():
                vector[k] *= math.log(float(N) / df[k], N)

        print 'tf-idf weights : '
        pprint.pprint(vectors)
        print ''

        q = {}
        for (term, freq) in self.query.items():
            q[term] = (self.alpha * freq)

        for vector in vectors:
            for (term, freq) in vector.items():
                if freq < 0:
                    temp = self.gamma * vector[term]
                else:
                    temp = self.beta * vector[term]
                if term in q:
                    q[term] += temp
                else:
                    q[term] = temp

        new_q = {}
        for (term, freq) in q.items():
            if freq > 0:
                new_q[term] = freq
        self.query = sorted(new_q.items(), key=operator.itemgetter(1), reverse=True)

        print 'new query : '
        pprint.pprint(self.query)

    def get_precision(self):
        return self.Dr/10.0
