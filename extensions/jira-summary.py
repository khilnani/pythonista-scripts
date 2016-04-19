# coding: utf-8


import json
import re
# pip install requests[security] --upgrade
import requests
import logging
import sys
import base64
import urllib2
import getpass

CONF_FILE = 'jira.conf'
JIRA_PAT = re.compile('([a-zA-Z]+-[0-9]+)')


def get_base_url():
    with open(CONF_FILE, 'r') as conf_file:
        try:
            conf = json.load(conf_file)
            return conf['BASE_URL']
        except Exception as e:
            logging.error('Config load error:')
            logging.error(e)
            sys.exit()

def main():
    text = None
    if len(sys.argv) > 1:
        text = sys.argv[1]
    
    if text:
        ids = JIRA_PAT.findall(text)
        if len(ids) > 0:
            id = ids[0]
            base_url = get_base_url()
            rest_url = '%s/rest/api/2/issue/%s' % (base_url, id)
            print(rest_url)
            u = raw_input('user:')
            p = getpass.getpass('pass:')
            if u and p:
                encoded = base64.encodestring('%s:%s' % (u,p))
                headers={
                        'Content-Type': 'application/json',
                        'Authorization': ('Basic %s' % encoded).replace('\n','')
                        }
                try:
                    request = urllib2.Request(rest_url, headers=headers)
                    response = urllib2.urlopen(request).read()
                    j = json.loads(response)
                    print j['fields']['summary']
                except urllib2.URLError as e:
                    print e

                try:
                    r = requests.get(rest_url, auth=(u, p))
                    j = r.json()
                    print j['fields']['summary']
                except requests.exceptions.SSLError as e:
                    print e
        else:
            print('No Jira ID found.')
    else:
        print('No input text found.')

if __name__ == '__main__':
    main()
