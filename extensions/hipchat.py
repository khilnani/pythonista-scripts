# coding: utf-8

"""
Description:
A python script to perform basic interactions with Hipchat.

License:
The MIT License (MIT)
Copyright (c) 2016 Nik Khilnani

Github:
https://github.com/khilnani/pythonista-scripts/

Configuration:
Rename 'hipchat.sample.conf' to 'hipchat.conf' and update values

To use:
1 - In any app, use App Share, Run in Pythonista and then select this script.
2 - Run this script from within Pythonista or a unix/linux terminal/console. 
"""

# https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens
# https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-title-expansion
# https://www.hipchat.com/docs/apiv2

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

CONF_FILE = 'hipchat.conf'

def df(s):
    sf = s
    try:
        d = dateutil.parser.parse(s)
        sf = d.strftime('%d/%m/%Y %H:%M:%S')
    except Exception as e:
        print (e)
    return sf

def update_conf_info(token, user=None):
    api_url, base_url, username, access_token = get_conf_info()
    conf = {}
    if api_url:
        conf['API_URL'] = api_url
    if base_url:
        conf['BASE_URL'] = base_url
    if user:
        conf['USER'] = user
    elif username:
        conf['USER'] = username
    if token:
        conf['ACCESS_TOKEN'] = token
        
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
            api_url = conf['API_URL']
            base_url = conf['BASE_URL']
            try:
                username = conf['USER']
            except KeyError:
                username = None
            try:
                access_token = conf['ACCESS_TOKEN']
            except KeyError:
                access_token = None
            return (api_url, base_url, username, access_token)
    except IOError:
        logging.error('Could not find %s' % CONF_FILE)
        sys.exit()

def get_new_access_token(api_url, base_url, username=None):
    print('Updating access token ...')
    if not username:
        username = raw_input('Username:')
    print('Tip: Get a personal access token from: https://www.hipchat.com/account/api')
    access_token = getpass.getpass('Access token:')
    update_conf_info(access_token, username)
    return access_token

def check_access_token(api_url, access_token):
    print('Checking access token ...')
    url = '%suser?auth_token=%s&auth_test=true' % (api_url, access_token)
    r = requests.get(url)
    valid = r.status_code >= 200 and r.status_code < 400
    print('Valid: %s' % valid)
    return valid

def main():
    cmd = None
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    else:
        try:
            import appex
            import clipboard
            if appex.is_running_extension():
                if appex.get_url():
                    cmd = appex.get_url()
                else:
                    cmd = appex.get_text()
            else:
                cmd = clipboard.get()
        except ImportError:
            pass

        api_url, base_url, username, access_token = get_conf_info() 
        
        if check_access_token(api_url, access_token):
            pass
        else:
            access_token = get_new_access_token(api_url, base_url, username)
            check_access_token(api_url, access_token)

if __name__ == '__main__':
    main()
