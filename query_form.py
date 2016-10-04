import math
import pprint
import operator
import parameters

class query_form(object):
    """docstring for ClassName"""

    def __init__(self, query):
        self.relevant_set = []
        self.non_relevant_set = []
        self.query = query


    def add_relevant_doc(self, doc):
        self.relevant_set.append(doc)

    def add_non_relevant_doc(self, doc):
        self.non_relevant_set.append(doc)

    def form_query(self):
        vectors = {}
        tf_r = {}
        tf_nr = {}
        df = {}
        N = 10
        docs_r = parameters.param.parser(self.relevant_set)
        docs_nr = parameters.param.parser(self.non_relevant_set)
        # count the frequency of each term in relevant docs

        for doc in docs_r:
            for term in doc:
                if term in tf_r:
                    tf_r[term] += 1
                else:
                    tf_r[term] = 1

        # count the frequency of each term in irrelevant docs
        for doc in docs_nr:
            for term in doc:
                if term in tf_nr:
                    tf_nr[term] += 1
                else:
                    tf_nr[term] = 1

        for doc in docs_r+docs_nr:
            for term in set(doc):
                if term in df:
                    df[term] += 1
                else:
                    df[term] = 1
                    vectors[term] = 0.0

        print self.query
        # calculate tf_ij
        for (term, freq) in self.query.items():
            vectors[term] = (parameters.param.alpha * freq)

        for term in tf_r:
            vectors[term] += parameters.param.beta *float(tf_r[term])*math.log(float(parameters.param.num)/(df[term]))

        for term in tf_nr:
            vectors[term] -= parameters.param.gamma * float(tf_nr[term])*math.log(float(parameters.param.num)/(df[term]))

        print 'weights :'
        pprint.pprint(vectors)
        print ''

        q = {key: vectors[key] for key in vectors if vectors[key] > 0}
        new_q = sorted(q.items(), key=operator.itemgetter(1), reverse=True)

        cnt = 0
        for (term, freq) in new_q:
            if cnt > 2:
                break;
            if term in self.query:
                self.query[term] += freq
            elif term not in self.query and len(term)<10:
                self.query[term] = freq
                cnt += 1

        return self.query