# coding: utf-8

"""
Description:
A python script to parse clipboard or shared text for jira ids 
and then output key info for that jira ticket instantly.

License:
The MIT License (MIT)
Copyright (c) 2016 Nik Khilnani

Github:
https://github.com/khilnani/pythonista-scripts/

Configuration:
Rename 'jira.sample.conf' to 'jira.conf' and update values

To use:
1 - In any app, use App Share, Run in Pythonista and then select this script
2 - Copy text with a Jira ID and run this script in Pythonista.
3 - Run this script in a linux/os x terminal with the JIRA ID as a command line arg
    eg. python jira.py ST-1222
"""

# Overview https://developer.atlassian.com/jiradev/jira-apis/jira-rest-apis
# General API https://docs.atlassian.com/jira/REST/latest/
# Agile API https://docs.atlassian.com/jira-software/REST/latest/

import json
import re
# pip install requests[security] --upgrade
import logging
import sys
import urllib2
import getpass
# pip install python-dateutil
import dateutil.parser
import datetime
import requests

CONF_FILE = 'jira.conf'
JIRA_PAT = re.compile('([a-zA-Z]+-[0-9]+)')

def df(s):
    sf = s
    try:
        d = dateutil.parser.parse(s)
        sf = d.strftime('%d/%m/%Y %H:%M:%S')
    except Exception as e:
        print (e)
    return sf

def update_conf_info(id, user=None):
    base_url, username, jsessionid = get_conf_info()
    conf = {}
    if base_url:
        conf['BASE_URL'] = base_url
    if user:
        conf['USER'] = user
    elif username:
        conf['USER'] = username
    if id:
        conf['JSESSIONID'] = id
        
    try:
        with open(CONF_FILE, 'w') as conf_file:
            #print(conf)
            json.dump(conf, conf_file)
    except IOError:
        logging.error('Could not write %s' % CONF_FILE)
        sys.exit()

def get_conf_info():
    try:
        with open(CONF_FILE, 'r') as conf_file:
            conf = json.load(conf_file)
            base_url = conf['BASE_URL']
            try:
                username = conf['USER']
            except KeyError:
                username = None
            try:
                jsessionid = conf['JSESSIONID']
            except KeyError:
                jsessionid = None
            return (base_url, username, jsessionid)
    except IOError:
        logging.error('Could not find %s' % CONF_FILE)
        sys.exit()

def get_new_cookie(base_url, username=None):
    print('Updating session ...')
    url = '%s/rest/auth/1/session' % base_url
    if not username:
        username = raw_input('Username:')
    password = getpass.getpass('Password:')
    body = {"username": username, "password":password}
    r = requests.post(url, json=body)
    jsessionid = r.cookies['JSESSIONID']
    update_conf_info(jsessionid, username)
    return jsessionid

def get(base_url, jsessionid, path):
    url = base_url + path
    try:
        r = requests.get(url, cookies={'JSESSIONID':jsessionid})
        valid = r.status_code >= 200 and r.status_code < 400
        return (valid, r)
    except ValueError as e:
        print e
        print r.headers
        sys.exit(e)
    except requests.exceptions.SSLError as e:
        print e
        sys.exit(e)

def check_jsessionid(base_url, jsessionid):
    print('Checking session ...')
    path = '/rest/api/2/myself'
    valid, r = get(base_url, jsessionid, path)
    return valid

def get_issue_info(base_url, jsessionid, key):
    print('Getting jira issue data ...')
    path = '/rest/api/2/issue/%s' % key
    http_url = '%s/browse/%s' % (base_url, key) 
    jira_data = None
    valid, r = get(base_url, jsessionid, path)
    if valid:
        jira_data = r.json()
    else:
        print('Issue not found.')
        sys.exit(1) 
    
    try:
        f = jira_data['fields']
        print('--------------------------------------')
        print('Link: %s' % http_url)
        print('Summary: %s' % f['summary'])
        print('Status: %s' % f['status']['name'])
        print('Priority: %s' % f['priority']['name'])
        print('Reporter: %s' % f['reporter']['displayName'])
        print('Created: %s' % df(f['created']))
        if f['assignee']:
            print('Assignee: %s' % f['assignee']['displayName'])
        else:
            print('Assignee: None')
        print('Labels: %s' % f['labels'])
        c_str= ''
        for c in f['components']:
            c_str = c['name'] + ', '
        print('Components:[%s]' % c_str)
        print('Description: %s' % f['description'])
        print('--------------------------------------')
        print('Links: ')
        for link in f['issuelinks']:
            _rel = link['type']['name']
            try:
                _li = link['inwardIssue']
            except KeyError:
                _li = None
            try:
                if not _li:
                    _li = link['outwardIssue']
            except KeyError:
                _li = None
            if _li:
                _key = _li['key']
                _lf = _li['fields']
                _summary = _lf['summary']
                _status = _lf['status']['name']
                _priority= _lf['priority']['name']
            else:
                _key = _summary = _status = _priority = ''
            print(_key, _status, _priority, _rel, _summary)
        print('--------------------------------------')
        print('Comments:')
        for c in f['comment']['comments']:
            a = c['author']['displayName']
            u = df(c['updated'])
            print('By %s on %s:' % (a,u))
            b = c['body']
            print('- ' + b)
            print('')
        print('--------------------------------------')
    except TypeError as e:
        print(str(e))
    except KeyError as e:
        print('Missing data: ' + str(e))
    
def main():
    text = None
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        try:
            import appex
            import clipboard
            if appex.is_running_extension():
                if appex.get_url():
                    text = appex.get_url()
                else:
                    text = appex.get_text()
            else:
                text = clipboard.get()
        except ImportError:
            pass
    
    if text:
        keys = JIRA_PAT.findall(text)
        if len(keys) > 0:
            key = keys[0]
            print('Found Jira ID: %s' % key)
        else:
            key = raw_input('Jira ID:')
        
        base_url, username, jsessionid = get_conf_info() 
        
        if check_jsessionid(base_url, jsessionid):
            get_issue_info(base_url, jsessionid, key)
        else:
            jsessionid = get_new_cookie(base_url, username)
            get_issue_info(base_url, jsessionid, key)     
    else:
        print('No input text found.')

if __name__ == '__main__':
    main()