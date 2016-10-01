import urllib2
import base64
import sys
import query_form
import json

def process_raw_query(raw_query):
    temp = raw_query.split();
    rst = {}
    for term in temp:
        rst[term] = 1
    return rst


def compose_url(query):
    bing_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query='
    for (term, freq) in query.items():
        bing_url += ('%27'+term)
    bing_url += "%27&$top=10&$format=json"
    return bing_url


def get_result(resp):
    # parse response to get all formatted result
    json_result = json.loads(resp)
    result_list = json_result['d']['results']

    result = []
    count = 0
    for data in result_list:
        row = {}
        count += 1
        row['Url'] = data['Url']
        row['Title'] = data['Title']
        row['Description'] = data['Description']
        print '======================================'
        print 'Result ', count
        print ' Url          :', row['Url']
        print ' Title        :', row['Title']
        print ' Description  :', row['Description']
        print '======================================'
        row['Feedback'] = raw_input('Relevant (Y/N)?').lower()
        result.append(row)
    return result

if __name__ == "__main__":

    accountKey = 'HIWkFhlcqfV0SsO9ac7smysylCtGDsuMVyqgSWPPDZI'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}

    raw_query = sys.argv[2].split()
    query = process_raw_query(raw_query)
    exp_precision = float(sys.argv[1])
    cur_precision = 0.01
    N = 10

    while cur_precision< exp_precision and cur_precision != 0:
        cur_url = compose_url(query)
        req = urllib2.Request(cur_url, headers=headers)
        resp = urllib2.urlopen(req).read()
        new_query = query_form(query)
        cur_precision = 0;

        for row in get_result(resp):
            if row['Feedback'] == 'y':
                new_query.add_relevant_doc(row['Description'])
                cur_precision += 1
            else:
                new_query.add_non_relevant_doc(row['Description'])

        cur_precision = float(cur_precision)/N
        query = new_query.form_query()

    if cur_precision == 0:
        print 'Below desired precision, but can no longer augment the query'
    else:
        print 'Satisfy the demanding precision'



