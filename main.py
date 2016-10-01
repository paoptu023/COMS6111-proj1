import urllib2
import base64
import sys
import query_form


def compose_url(query):
    bing_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query='
    for item in query:
        bing_url += ('%27'+item)
    bing_url += "%27&$top=10&$format=json"
    return bing_url


def get_result(resp):
    # parse response to get all formatted result
    result = {}
    return result


def print_result(rst):
    print 'Result', id + 1
    print '['
    for key in ['Url', 'Title', 'Description']:
        print '', key, ':', rst[key].encode("utf-8")
    print ']'
    print
    feedback = raw_input('Relevant (Y/N)?')
    print "You entered", feedback
    print ''
    return feedback


if __name__ == "__main__":

    accountKey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
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

        for (id, rst) in enumerate(get_result(resp)):
            user_fb = print_result(rst)
            if user_fb.lower() == 'y':
                new_query.add_relevant_doc(rst['Description'])
                cur_precision += 1
            else:
                new_query.add_non_relevant_doc(rst['Description'])

        cur_precision = new_query.get_precision()
        query = new_query.form_query()

    if cur_precision == 0:
        print 'Below desired precision, but can no longer augment the query'
    else:
        print 'Satisfy the demanding precision'



