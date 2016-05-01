# coding: utf-8

"""
Description:
Parse text to pull out jira ID and launch a browser with the URL to the Jira issue.
Supports App Share, or clipboard

License:
The MIT License (MIT)
Copyright (c) 2016 Nik Khilnani

Github:
https://github.com/khilnani/pythonista-scripts/

Configuration:
Rename 'jira.sample.conf' to 'jira.conf' and update values

To use:
1 - In any app, use App Share, Run in Pythonista and then select this script
2 - Copy text with a Jira ID and run this script within Pythonista. 
"""

import appex
import clipboard, console, webbrowser, re, json
from objc_util import *

CONF_FILE = 'jira.conf'
JIRA_PAT = re.compile('([a-zA-Z]+-[0-9]+)')


def get_jira_info():
    try:
        with open(CONF_FILE, 'r') as conf_file:
            conf = json.load(conf_file)
            url = conf['BASE_URL']
            try:
                user = conf['USER']
            except KeyError:
                user = None
            return (url, user)
    except IOError:
        logging.error('Could not find %s' % CONF_FILE)
        sys.exit()

def main():
    if appex.is_running_extension():
        if appex.get_url():
            text = appex.get_url()
        else:
            text = appex.get_text()
    else:
        text = clipboard.get()
    if text:
        ids = JIRA_PAT.findall(text)
        if len(ids) > 0:
            id = ids[0]
            base_url, username = get_jira_info()
            url = '%s/browse/%s' % (base_url, id)
            console.hud_alert('Jira ID: %s' % id)
            app=UIApplication.sharedApplication()
            url=nsurl(url)
            app.openURL_(url)
        else:
            console.hud_alert('No Jira ID found.')
    else:
        console.hud_alert('No input text found.')
    if appex.is_running_extension():
        appex.finish()

if __name__ == '__main__':
    main()
