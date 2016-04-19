# coding: utf-8

import appex
import clipboard, console, webbrowser, re, json
from objc_util import *

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
    if not appex.is_running_extension():
        text = clipboard.get()
    else:
        text = appex.get_text()
    if text:
        ids = JIRA_PAT.findall(text)
        if len(ids) > 0:
            id = ids[0]
            base_url = get_base_url()
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
