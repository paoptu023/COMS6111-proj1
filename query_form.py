import math
import pprint
import operator
import parameters

class query_form(object):
    """docstring for ClassName"""

    def __init__(self, query):
        self.relevant_set_des = []
        self.non_relevant_set_des = []
        self.relevant_set_title = []
        self.non_relevant_set_title = []
        self.relevant_set_url = []
        self.non_relevant_set_url = []
        self.query = query

    def add_relevant_doc(self, title, des, url):
        self.relevant_set_title.append(title)
        self.relevant_set_des.append(des)
        self.relevant_set_url.append(url)

    def add_non_relevant_doc(self, title, des, url):
        self.non_relevant_set_title.append(title)
        self.non_relevant_set_des.append(des)
        self.non_relevant_set_url.append(url)

    def add_freq(self, docs, tf, w):
        for doc in docs:
            for term in doc:
                if term in tf:
                    tf[term] += w
                else:
                    tf[term] = w
        return tf

    def form_query(self):
        vectors = {}
        tf_r = {}
        tf_nr = {}
        df = {}

        des_docs_r = parameters.param.parser(self.relevant_set_des)
        des_docs_nr = parameters.param.parser(self.non_relevant_set_des)
        title_docs_r = parameters.param.parser(self.relevant_set_title)
        title_docs_nr = parameters.param.parser(self.non_relevant_set_title)
        url_docs_r = parameters.param.parseURL(self.relevant_set_url)
        url_docs_nr = parameters.param.parseURL(self.non_relevant_set_url)

        # count the frequency of each term in docs
        self.add_freq(des_docs_r, tf_r, 1)
        self.add_freq(title_docs_r, tf_r, 1)
        self.add_freq(url_docs_r, tf_r, 1)
        self.add_freq(des_docs_nr, tf_nr, 1)
        self.add_freq(title_docs_nr, tf_nr, 1)
        self.add_freq(url_docs_nr, tf_nr, 1)

        for i in range(0, len(des_docs_r)):
            for term in set(des_docs_r[i]).union(set(title_docs_r[i])).union(set(url_docs_r[i])):
                if term in df:
                    df[term] += 1
                else:
                    df[term] = 1
                    vectors[term] = 0.0

        for i in range(0, len(des_docs_nr)):
            for term in set(des_docs_nr[i]).union(set(title_docs_nr[i])).union(set(url_docs_nr[i])):
                if term in df:
                    df[term] += 1
                else:
                    df[term] = 1
                    vectors[term] = 0.0

        # calculate tf_ij
        for (term, freq) in self.query.items():
            vectors[term] = (parameters.param.alpha * freq)

        for term in tf_r:
            vectors[term] += parameters.param.beta *float(tf_r[term])*math.log(float(parameters.param.num)/(df[term]))

        for term in tf_nr:
            vectors[term] -= parameters.param.gamma * float(tf_nr[term])*math.log(float(parameters.param.num)/(df[term]))

        q = {key: vectors[key] for key in vectors if vectors[key] > 0}
        new_q = sorted(q.items(), key=operator.itemgetter(1), reverse=True)
        print 'weights :'
        pprint.pprint(new_q)

        cnt = 0
        for (term, freq) in new_q:
            if term in self.query:
                self.query[term] += freq
            elif term not in self.query and cnt < 2:
                self.query[term] = freq
                cnt += 1

        return self.query
