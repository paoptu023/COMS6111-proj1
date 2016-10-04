import re

class param(object):
    """docstring for ClassName"""

    stop_words = set()
    alpha = 1
    beta = 0.75
    gamma = 0.15
    num = 10

    @staticmethod
    def read_stop_words():
        f = open('stopwords.txt', 'r')
        for word in f.read().split():
            param.stop_words.add(word)

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