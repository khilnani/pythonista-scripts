# coding: utf-8

import console, clipboard
from objc_util import *

def main():
    console.hud_alert('Saving clipboard to Evernote.')
    text = clipboard.get().strip()
    _eurl = "evernote://x-callback-url/new-note?type=clipboard&title=DRAFT&text="
    app=UIApplication.sharedApplication()
    eurl=nsurl(_eurl)
    app.openURL_(eurl)

if __name__ == '__main__':
    main()