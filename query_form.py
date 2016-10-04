import math
import pprint
import operator
import re

class query_form(object):
    """docstring for ClassName"""

    def __init__(self, query):
        self.relevant_set = set()
        self.non_relevant_set = set()
        self.query = query
        self.alpha = 1
        self.beta = 0.75
        self.gamma = 0.15
        f = open('stopwords.txt', 'r')
        self.stop_words = set()
        for word in f.read().split():
            self.stop_words.add(word)

    def add_relevant_doc(self, doc):
        self.relevant_set.add(doc)

    def add_non_relevant_doc(self, doc):
        self.non_relevant_set.add(doc)
    
    def add_freq(self, d, t_set, total_set, d_set, w):
        doc = ''
        for term in d.split():
            if term in self.stop_words:
                doc += ' '
            else:
                doc += str(term).lower() + ' '
    
        for term in doc.split():
            if term in t_set:
                t_set[term] += w
            else:
                t_set[term] = w
            if term in total_set:
                total_set[term] += w
            else:
                total_set[term] = w
    
        for term in set(doc.split()):
            if term in d_set:
                d_set[term] += w
            else:
                d_set[term] = w

    def form_query(self):
        vectors = {}
        total_tf = {}
        tf_r = {}
        tf_nr = {}
        df_r = {}
        df_nr = {}
        N = 10

        # count the frequency of each term in relevant docs
        for d in self.relevant_set:
            title = re.sub('[^a-z]+', ' ', d[0].lower()) # need to be discussed
            description = re.sub('[^a-z]+', ' ', d[1].lower())
            self.add_freq(title, tf_r, total_tf, df_r, 1.5)
            self.add_freq(description, tf_r, total_tf, df_r, 1)

        # count the frequency of each term in irrelevant docs
        for d in self.non_relevant_set:
            title = re.sub('[^a-z]+', ' ', d[0].lower()) # need to be discussed
            description = re.sub('[^a-z]+', ' ', d[1].lower())
            self.add_freq(title, tf_nr, total_tf, df_nr, 1.5)
            self.add_freq(description, tf_nr, total_tf, df_nr, 1)

        pprint.pprint(tf_r)
        pprint.pprint(tf_nr)
        pprint.pprint(df_r)
        pprint.pprint(df_nr)
        print ''

        # calculate tf_ij
        for (term, freq) in total_tf.items():
            vectors[term] = 0.0

        for (term, freq) in self.query:
            vectors[term] = (self.alpha * freq)

        for term in tf_r:
            vectors[term] += self.beta *(float(tf_r[term]) )*math.log(float(N)/df_r[term])
#/ total_tf[term]
        for term in tf_nr:
            vectors[term] -= self.gamma * (float(tf_nr[term]) )*math.log(float(N)/df_nr[term])

        print 'weights :'
        pprint.pprint(vectors)
        print ''

        q = {key: vectors[key] for key in vectors if vectors[key] > 0}
        new_q = sorted(q.items(), key=operator.itemgetter(1), reverse=True)

        dict_q = dict((k,v) for (k,v) in self.query)

        '''
        avg = 0;
        for (term, freq) in self.query:
            avg += freq
        avg /= len(self.query)
        '''

        cnt = 0
        for (term, freq) in new_q:
            if cnt > 2:
                break;
            if term in dict_q:
                dict_q[term] += freq
            elif term not in dict_q and len(term)<10:
                dict_q[term] = freq
                cnt += 1

        return dict_q.items()
