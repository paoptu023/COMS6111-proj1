import re
import parameters
import sys

doc = 'Hello word! wiki-a 1234'
#d = re.sub('[^a-z]+', ' ', doc.lower())
d = re.sub('[^a-zA-Z\n\.]', ' ', doc)
print d
#print d.split()
parameters.param.read_stop_words()
rst =  parameters.param.parser(doc)
print rst

sys.exit('Opps, something went wrong, consider another query')

self.non_relevant_set_des = []
self.relevant_set_title = []