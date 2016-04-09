# coding: utf-8
## Download a url in printable text format
## https://forum.omz-software.com/topic/2648/download-plain-text-html-document-and-save-content-as-text


import os, sys, re, random, appex, console, clipboard, html2text, requests, dialogs, urllib 
from objc_util import *

GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

def main():
    if appex.is_running_extension():
        url = appex.get_url()
        if url == None:
          text = appex.get_text()
          url = [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(text) ][0]
    else:
        text = clipboard.get().strip()
        url = [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(text) ][0]
        if not "http" in url:
            url = "http://"
        try:
            url = console.input_alert("URL", "", url)
        except:
            return True

    console.hud_alert('URL: %s' % url)

    h = html2text.HTML2Text()
    try:
        r = requests.get(
            url=url, 
            headers={"User-agent": "Mozilla/5.0{0:06}".format(random.randrange(999999))}
        )
    except Exception as e:
        console.alert(e.message)
        return True

    html_content = r.text.decode('utf-8')
    rendered_content = html2text.html2text(html_content)
    clipboard.set(rendered_content)

    launch_e = console.alert('Markdown copied to clipboard. Launch Evernote?', button1='Yes', button2='No', hide_cancel_button=True)
    if launch_e ==1:
        _eurl = "evernote://x-callback-url/new-note?type=clipboard&title=DRAFT&text="
        app=UIApplication.sharedApplication()
        eurl=nsurl(_eurl)
        app.openURL_(eurl)
    appex.finish()

if __name__ == '__main__':
    main()