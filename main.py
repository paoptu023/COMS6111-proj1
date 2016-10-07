import urllib2
import base64
import sys
import query_processor
import json
import parameters
import re
import operator
from urlparse import urlparse


# parse the initial input query
def process_raw_query(raw):
    print 'Parsing the input query ... '
    temp = raw.lower().split()
    rst = {}
    for term in temp:
        rst[term] = 1
    return rst


# compose the query url
def compose_url(query_dic, n):
    print 'Composing the query url ... '
    bing_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'
    for (term, freq) in query_dic.items():
        bing_url += '+'+term
    bing_url += '%27&$top=' + str(n) + '&$format=json'
    return bing_url


# parse the query response to get formatted results
def get_result(response, transcript):
    json_result = json.loads(response)
    result_list = json_result['d']['results']
    result = []
    count = 0
    for data in result_list:
        temp = {}
        count += 1
        temp['Url'] = data['Url']
        temp['Title'] = data['Title']
        temp['Description'] = data['Description']
        print '======================================'
        transcript.write('======================================\n')
        print 'Result ', count
        transcript.write('Result %d\n' % count)
        print 'Url          : ', temp['Url']
        transcript.write('Url          : %s\n' % temp['Url'].encode('utf8'))
        print 'Title        : ', temp['Title']
        transcript.write('Title          : %s\n' % temp['Title'].encode('utf8'))
        print 'Description  : ', temp['Description']
        transcript.write('Description          : %s\n' % temp['Description'].encode('utf8'))
        print '======================================'
        transcript.write('======================================\n')
        while 1:
            fb = raw_input('Relevant (Y/N)?').lower()
            if fb == 'y' or fb == 'n':
                temp['Feedback'] = fb
                transcript.write('Feedback: %s\n' % fb)
                break
            else:
                print 'Please input Y/N to indicate the relevance'
        result.append(temp)
    return result


# parse url, get the last two components, remove digits and special characters
def parse_url(url):
    path = urlparse(url).path.replace('.html', '')
    path = ''.join(i for i in path if not i.isdigit())
    result = path.split('/')[-1] + ' ' + path.split('/')[-2]
    result = re.sub('[^a-zA-Z\n\.]', ' ', result)
    return result


def main():
    transcript = open("cur_transcript.txt", "a")
    # parse accountKey
    account_key = sys.argv[1]
    account_key_encry = base64.b64encode(account_key + ':' + account_key)
    headers = {'Authorization': 'Basic ' + account_key_encry}

    # get input precision
    exp_precision = float(sys.argv[2])
    # parse raw query
    raw_query = ' '.join(sys.argv[3:])
    query = process_raw_query(raw_query)

    cur_precision = 0.01
    parameters.param.read_stop_words()

    while exp_precision > cur_precision and cur_precision != 0:
        print 'Query is: ', query
        transcript.write('Query is: {')
        for key, value in query.items():
            transcript.write('%s:%s ' % (key, value))
            transcript.write('}\n')

        # query bing to get results
        cur_url = compose_url(query, parameters.param.num)
        req = urllib2.Request(cur_url, headers=headers)
        resp = urllib2.urlopen(req).read()

        # form new query process object and initialize the relative parameters
        helper = query_processor.processor(query)
        cur_precision = 0

        # classify the result docs
        for row in get_result(resp, transcript):
            if row['Feedback'] == 'y':
                helper.add_relevant_doc(row['Title'] + ' ' + row['Description'] + ' ' + parse_url(row['Url']))
                cur_precision += 1
            else:
                helper.add_non_relevant_doc(row['Title'] + ' ' + row['Description'] + ' ' + parse_url(row['Url']))

        # calculate the new precision
        cur_precision = float(cur_precision)/parameters.param.num
        print 'Current precision of relevance is : ', cur_precision
        transcript.write('Current precision of relevance is : %f\n' % cur_precision)

        #
        if cur_precision == 0:
            transcript.write('Opps, none relevant docs found, consider another query\n')
            sys.exit('Opps, none relevant docs found, consider another query')
        else:
            query = helper.form_query()

    # the program terminates when no relevant doc found or achieve the expected precision
    print 'Achieved the required precision'
    transcript.write('Achieved the required precision\n\n')
    transcript.close()
    exit()

# entrance of the program
if __name__ == "__main__":
    main()
