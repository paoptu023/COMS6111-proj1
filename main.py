import urllib2
import base64
import sys
import query_form
import json


def compose_url(query):
    bing_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query='
    for item in query:
        bing_url += ('%27'+item)
    bing_url += "%27&$top=10&$format=json"
    return bing_url


def get_result(resp):
    # parse response to get all formatted result
    json_result = json.loads(resp)
    result_list = json_result['d']['results']

    result = []
    for data in result_list:
        row = {}
        row['Url'] = data['Url']
        row['Title'] = data['Title']
        row['Description'] = data['Description']
        row['Feedback'] = raw_input('Relevant (Y/N)?').lower()
        result.append(row)
    return result


def print_result(rst):
    print 'Result', id + 1
    print '['
    for key in ['Url', 'Title', 'Description']:
        print '', key, ':', rst[key].encode("utf-8")
    print ']'
    print
    
    print "You entered", feedback
    print ''
    return feedback


if __name__ == "__main__":

    accountKey = 'HIWkFhlcqfV0SsO9ac7smysylCtGDsuMVyqgSWPPDZI'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}

    query = raw_q = sys.argv[2].split()
    exp_precision = float(sys.argv[1])
    cur_precision = 0.01

    while cur_precision< exp_precision and cur_precision != 0:
        cur_url = compose_url(query)
        req = urllib2.Request(cur_url, headers=headers)
        resp = urllib2.urlopen(req).read()
        new_query = query_form(query)

        for tuple in get_result(resp):
            if tuple['Feedback'] == 'y':
                new_query.add_relevant_doc(tuple['Description'])
                cur_precision += 1
            else:
                new_query.add_non_relevant_doc(tuple['Description'])

        cur_precision = new_query.get_precision()
        query = new_query.form_query()

    if cur_precision == 0:
        print 'Below desired precision, but can no longer augment the query'
    else:
        print 'Satisfy the demanding precision'



