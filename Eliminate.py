f = open('stopwords.txt', 'r')
stop_words = set()

for word in f.read().split():
    stop_words.add(word)
    print stop_words
