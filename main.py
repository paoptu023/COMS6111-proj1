import urllib2
import base64
import sys
import query_form
import json
import pprint


def process_raw_query(raw_query):
    temp = raw_query.split();
    rst = {}
    for term in temp:
        rst[term] = 1
    return rst


def compose_url(query, N):
    bing_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'
    print type(query), query
    for (term, freq) in query:
        bing_url += '+'+term
    bing_url += '%27&$top=' + str(N) + '&$format=json'
    print bing_url
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

    raw_query = 'Taj Mahal'#sys.argv[2]
    query = process_raw_query(raw_query.lower()).items()
    exp_precision = 1#float(sys.argv[1])
    cur_precision = 0.01
    N = 10

    while exp_precision > cur_precision and cur_precision != 0:
        print cur_precision
        print 'new query : '
        pprint.pprint(query)
        cur_url = compose_url(query, N)
        req = urllib2.Request(cur_url, headers=headers)
        resp = urllib2.urlopen(req).read()
        new_query = query_form.query_form(query)
        cur_precision = 0;
        for row in get_result(resp):
            if row['Feedback'] == 'y':
                new_query.add_relevant_doc((row['Title'], row['Description']))
                cur_precision += 1
            else:
                new_query.add_non_relevant_doc((row['Title'], row['Description']))
        cur_precision = float(cur_precision)/N
        if cur_precision == 0:
            break;
        else:
            query = new_query.form_query()

    if cur_precision == 0:
        print 'Opps, something went wrong, consider another query'
    else:
        print 'Achieved the required precision'



