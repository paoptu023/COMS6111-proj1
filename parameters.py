import re
from urlparse import urlparse

class param(object):
    """docstring for ClassName"""

    stop_words = set()
    alpha = 1
    beta = 0.75
    gamma = 0.15
    num = 10
    url = {}

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
                    temp.append(str(term))
            rst.append(temp)
        return rst

    @staticmethod
    def parseURL(urls):
        rst = []
        for url in urls:
            path = urlparse(url).path.replace('.html', '')
            path = ''.join(i for i in path if not i.isdigit())
            result = path.split('/')[-1] + ' ' + path.split('/')[-2]
            result = re.sub('[^a-zA-Z0-9\n\.]', ' ', result)
            temp = []
            for term in result.lower().split():
                if term not in param.stop_words:
                    temp.append(str(term))
            rst.append(temp)
        return rst
