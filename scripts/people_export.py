''' people export'''

import base64
import csv
import sys
import time
import urllib # for url encoding
import urllib2 # for sending requests

try:
    import json
except ImportError:
    import simplejson as json

class Mixpanel(object):

    def __init__(self, api_secret):
        self.api_secret = api_secret

    def request(self, params, format='json'):
        '''let's craft the http request'''
        data = None
        request_url = 'https://mixpanel.com/api/2.0/engage/?'
        request_url = request_url + self.unicode_urlencode(params)
        headers = {'Authorization': 'Basic {encoded_secret}'.format(encoded_secret=base64.b64encode(self.api_secret))}
        request = urllib2.Request(request_url, data, headers)
        response = urllib2.urlopen(request, timeout=120)
        return response.read()

    def unicode_urlencode(self, params):
        ''' Convert stuff to json format and correctly handle unicode url parameters'''

        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        result = urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])
        return result

    def get_and_write_results(self, params):
        response = api.request(params)
        parameters['session_id'] = json.loads(response)['session_id']
        parameters['page'] = 0
        global_total = json.loads(response)['total']

        print "Session id is %s \n" % parameters['session_id']
        print "Here are the # of people %d" % global_total

        paged = self._page_results(response, parameters, global_total)
        self.export_csv("people_export_" + str(int(time.time())) + ".csv", paged)

    def _page_results(self, response, parameters, global_total):

        fname = "people_export_" + str(int(time.time())) + ".txt"
        parameters['page'] = 0
        has_results = True
        total = 0
        while has_results:
            responser = json.loads(response)['results']
            total += len(responser)
            has_results = len(responser) == 1000
            self._write_results(responser, fname)
            print "%d / %d" % (total, global_total)
            parameters['page'] += 1
            if has_results:
                response = api.request(parameters)
        return fname

    def _write_results(self, results, fname):
        with open(fname, 'a') as f:
            for data in results:
                f.write(json.dumps(data) + '\n')

    def export_csv(self, outfilename, fname):
        '''takes a file name of a file of json objects and the desired name of the csv file that will be written'''
        subkeys = set()
        with open(fname, 'rb') as r:
            with open(outfilename, 'wb') as w:
                # Get all properties (will use this to create the header)
                for line in r:
                    try:
                        subkeys.update(set(json.loads(line)['$properties'].keys()))
                    except:
                        pass

                # Create the header
                header = ['$distinct_id']
                for key in subkeys:
                    header.append(key.encode('utf-8'))

                # Create the writer and write the header
                writer = csv.writer(w)
                writer.writerow(header)

                # Return to the top of the file, then write the events out, one per row
                r.seek(0, 0)
                for line in r:
                    entry = json.loads(line)
                    row = []
                    try:
                        row.append(entry['$distinct_id'])
                    except:
                        row.append('')

                    for subkey in subkeys:
                        try:
                            row.append((entry['$properties'][subkey]).encode('utf-8'))
                        except AttributeError:
                            row.append(entry['$properties'][subkey])
                        except KeyError:
                            row.append("")
                    writer.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        api_secret = sys.argv[1]
    else:
        api_secret = raw_input("API Secret: ")

    api = Mixpanel(
        api_secret=api_secret
    )

    '''
    Here is the place to define your selector to target only the users that you're after
    selector = '(datetime(1458587013 - 86400) > properties["Created"] and behaviors["behavior_79"] > 0'
    behaviors = '[{"window": "90d", "name": "behavior_79", "event_selectors": [{"event": "Edit Colors"}]}]'
    '''
    selector = ''
    # Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
    behaviors = r''

    if not behaviors:
        parameters = {'selector': selector}
    else:
        time_offset = int(raw_input("Project time offset from GMT (ex. PST = -8): "))
        parameters = {'selector': selector, 'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

    api.get_and_write_results(parameters)
