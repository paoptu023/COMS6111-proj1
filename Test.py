import math

query = {'a':0.1, 'b':0.5}
relevant_set = ['a b c, y h', 'd e f','e e e']
non_relevant_set = {}
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
# count the frequency of each term
for d in relevant_set:
    doc = d.split()
    tf = {}
    for term in doc:
        if term in tf:
            tf[term] += 1
        else:
            tf[term] = 1
        if term in total_tf:
            total_tf[term] += 1
        else:
            total_tf[term] = 1
    vectors.append(tf)

# calculate tf_ij and idf
for vector in vectors:
    for (k,v) in vector.items():
        vector[k] = float(vector[k])/total_tf[k]
        if k in df:
            df[k] += 1
        else:
            df[k] = 1

print 'doc vectors : ', vectors

#calculate w_ij
for vector in vectors:
    for (k,v) in vector.items():
        vector[k] *= math.log(float(N)/df[k],N)

print 'doc vectors : ', vectors
q = {}
for (term, freq) in query.items():
    q[term] = (alpha*freq)

for vector in vectors:
    for (term,freq) in vector.items():
        if term in q:
            q[term] += (beta*vector[term])
        else:
            q[term] = (beta*vector[term])

print 'q : ',q