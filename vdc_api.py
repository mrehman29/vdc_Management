# -*- coding: utf-8 -*-
# try something like
from __future__ import print_function
import getpass,json, os, pprint,socket,struct,sys,base64,hashlib,hmac,time,urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

class VDCApiCall(object):
    def __init__(self, api_url, apiKey, secret):
        self.api_url = api_url
        self.apiKey = apiKey
        self.secret = secret

    def request(self, args):
        args['apiKey'] = self.apiKey

        request = zip(args.keys(), args.values())
        request.sort(key=lambda x: x[0].lower())
        request_data = "&".join(["=".join([r[0], urllib.quote_plus(str(r[1]))])
                                for r in request])
        hashStr = "&".join(
            [
                "=".join(
                    [r[0].lower(),
                     str.lower(urllib.quote_plus(str(r[1]))).replace(
                         "+", "%20"
                     )]
                ) for r in request
            ]
        )
        sig = urllib.quote_plus(base64.b64encode(
            hmac.new(
                self.secret,
                hashStr,
                hashlib.sha1
            ).digest()
        ).strip())

        request_data += "&signature=%s" % sig
        err = ''
        try:
            connection = urllib2.urlopen(self.api_url, request_data)
            response = connection.read()
        except urllib2.HTTPError as error:
            return error.read()
            ##err['01'] = 'HTTP Error:' + str(error.code)
            description = 'HTTP Error: %s' % error.code
            description = str(error.info())
            ##err['02'] = str(error.info())
            description = description.split('\n')
            description += [line
                           for line
                           in description
                           if line.startswith('X-Description: ')]

            if len(description) > 0:
                description += description[0].split(':', 1)[-1].lstrip()

            else:
                description += '(No extended error message.)'

        return response

    def wait_for_job(self, job_id, delay=2, display_progress=True):
        request = {
            'jobid': job_id,
        }
        while(True):
            result = self.queryAsyncJobResult(request)
            if display_progress:
                print('.', end='')
                sys.stdout.flush()
            if 'jobresult' in result:
                print('')
                return result['jobresult']
            time.sleep(delay)

    def wait_for_job_background(self, job_id, delay=2, display_progress=False):
        request = {
            'jobid': job_id,
        }

        while(True):
            result = self.queryAsyncJobResult(request)
            #if display_progress:
            #    print('.', end='')
            #    sys.stdout.flush()
            if 'jobresult' in result:
                #print('')
                return result['jobresult']
            time.sleep(delay)

    def __getattr__(self, name):
        def handlerFunction(*args, **kwargs):
            if kwargs:
                return self._make_request(name, kwargs)
            return self._make_request(name, args[0])
        return handlerFunction

    def _make_request(self, command, args):
        args['response'] = 'json'
        args['command'] = command
        data = self.request(args)
        key = command.lower() + "response"
        try:
            return json.loads(data)[key]
        except :
            return json.loads(data)

    def call(self,command, args):
        args['response'] = 'json'
        args['command'] = command
        data = self.request(args)
        key = command.lower() + "response"
        try:
            return json.loads(data)[key]
        except :
            return json.loads(data)
	
