import re

class param(object):
    """
    some commonly used parameters and methods
    """

    stop_words = set()
    alpha = 1
    beta = 0.75
    gamma = 0.15
    num = 10
    add_terms = 2

    @staticmethod
    def read_stop_words():
        f = open('stopwords.txt', 'r')
        for word in f.read().split():
            param.stop_words.add(word)

    # clean the stopwords and parse the string format documents to list format
    @staticmethod
    def parser(docs):
        rst = []
        for doc in docs:
            d = re.sub('[^a-z]+', ' ', doc.lower()).split()  # need to be discussed
            temp = []
            for term in d:
                if term not in param.stop_words:
                    temp.append(term)
            rst.append(temp)
        return rst