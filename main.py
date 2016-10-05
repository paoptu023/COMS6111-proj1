import urllib2
import base64
import sys
import query_processor
import json
import parameters
import re
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
def get_result(response):
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
        print 'Result ', count
        print ' Url          :', temp['Url']
        print ' Title        :', temp['Title']
        print ' Description  :', temp['Description']
        print '======================================'
        while 1:
            fb = raw_input('Relevant (Y/N)?').lower()
            if fb == 'y' or fb == 'n':
                temp['Feedback'] = fb
                break
            else:
                print 'Please input Y/N to indicate the relevance'
        result.append(temp)
    return result


def parseURL(url):
    path = urlparse(url).path.replace('.html', '')
    path = ''.join(i for i in path if not i.isdigit())
    result = path.split('/')[-1] + ' ' + path.split('/')[-2]
    result = re.sub('[^a-zA-Z0-9\n\.]', ' ', result)
    return result


def main():
    # parse accountKey
    account_key = 'HIWkFhlcqfV0SsO9ac7smysylCtGDsuMVyqgSWPPDZI' #sys.argv[1]
    account_key_encry = base64.b64encode(account_key + ':' + account_key)
    headers = {'Authorization': 'Basic ' + account_key_encry}

    # get input precision
    exp_precision = 1 #float(sys.argv[2])
    # parse raw query
    raw_query = 'brin' #sys.argv[3]
    query = process_raw_query(raw_query)

    cur_precision = 0.01
    parameters.param.read_stop_words()

    while exp_precision > cur_precision and cur_precision != 0:
        # query bing to get results
        cur_url = compose_url(query, parameters.param.num)
        req = urllib2.Request(cur_url, headers=headers)
        resp = urllib2.urlopen(req).read()

        # form new query process object and initialize the relative parameters
        helper = query_processor.processor(query)
        cur_precision = 0

        # classify the result docs
        for row in get_result(resp):
            if row['Feedback'] == 'y':
                helper.add_relevant_doc(row['Title'] + ' ' + row['Description'] + ' ' + parseURL(row['Url']))
                cur_precision += 1
            else:
                helper.add_non_relevant_doc(row['Title'] + ' ' + row['Description'] + ' ' + parseURL(row['Url']))

        # calculate the new precision
        cur_precision = float(cur_precision)/parameters.param.num
        print 'Current precision of relevance is : ',cur_precision

        #
        if cur_precision == 0:
            sys.exit('Opps, none relevant docs found, consider another query')
        else:
            query = helper.form_query()

    # the program terminates when no relevant doc found or achieve the expected precision
    print 'Achieved the required precision'
    exit()

# entrance of the program
if __name__ == "__main__":
    main()
