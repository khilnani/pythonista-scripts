# coding: utf-8

import appex
import clipboard, speech, console, html2text, requests, random, re

GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

def main():
    speech.stop()
    if not appex.is_running_extension():
        console.hud_alert('Reading clipboard')
        text = clipboard.get()
        url = None
    else:
        text = appex.get_text()
        url = appex.get_url()

    if url == None:
        try:
            url = [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(text) ][0]
        except:
            pass

    if url != None:
        console.hud_alert('Reading: ' + url)
        h = html2text.HTML2Text()
        try:
            r = requests.get(
            url=url,
            headers={"User-agent": "Mozilla/5.0{0:06}".format(random.randrange(999999))})
        except Exception as e:
            console.alert(e.message)
            return True
        html_content = r.text.decode('utf-8')
        text = html2text.html2text(html_content)
    else:
        console.hud_alert('Reading text: ' + str(text))

    if text:
        speech.say(text)
        stop = console.alert('Done?', hide_cancel_button=True, button1='OK')
        speech.stop()
    else:
        console.hud_alert('No text found.')

if __name__ == '__main__':
    main()
