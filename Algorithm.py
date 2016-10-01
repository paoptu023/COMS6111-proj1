import math
import pprint
import operator

query = {'a':0.1, 'b':0.5}
relevant_set = {'a b c, y h', 'd e f', 'e e e'}
non_relevant_set = {'i j k', 'e e e'}
Dr = 0
Dnr = 0
alpha = 1
beta = 2
gamma = 2

vectors = []
df = {}
total_tf = {}
N = 10
docs = []

docs = relevant_set.union(non_relevant_set)

# count the frequency of each term
for d in docs:
    doc = d.split()
    tf = {}
    cnt = 1;
    if d in non_relevant_set:
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
    for (k,v) in vector.items():
        vector[k] = float(vector[k])/total_tf[k]
        if k in df:
            df[k] += 1
        else:
            df[k] = 1

print 'normalized term frequency :'
pprint.pprint(vectors)
print ''
#calculate w_ij
for vector in vectors:
    for (k,v) in vector.items():
        vector[k] *= math.log(float(N)/df[k],N)

print 'tf-idf weights : '
pprint.pprint(vectors)
print ''

q = {}
for (term, freq) in query.items():
    q[term] = (alpha*freq)

for vector in vectors:
    for (term,freq) in vector.items():
        if freq < 0:
            temp = gamma*vector[term]
        else:
            temp = beta*vector[term]
        if term in q:
            q[term] += temp
        else:
            q[term] = temp

new_q = {}
for (term, freq) in q.items():
    if freq >0:
        new_q[term] = freq
query = sorted(new_q.items(), key=operator.itemgetter(1), reverse=True)

print 'new query : '
pprint.pprint(query)
