# coding: utf-8

import appex, clipboard, console
from markdown2 import markdown
import ui, scene, os

TEMPLATE = '''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>Preview</title>
<style type="text/css">
body {
    font-family: helvetica;
    font-size: 15px;
    margin: 10px;
}
</style>
</head>
<body>{{CONTENT}}</body>
</html>
'''

class MyWebView (ui.View):
    def load_html(self, html):
        wv = ui.WebView('Markdown Preview')
        wv.scales_page_to_fit = True
        wv.load_html(html)
        w, h = scene.get_screen_size()
        wv.width = w
        wv.height = h-60
        self.add_subview(wv)

    def will_close(self):
        if appex.is_running_extension():
            appex.finish()

def main():
    text = None
    label = 'Shared text'
    if appex.is_running_extension():
        text = appex.get_text()
    if not text:
        try:
            import editor
            editor_file = editor.get_path()
            if editor_file:
                sel = console.alert('Editor or clipboard?', button1='Editor', button2='Clipboard')
                if sel == 1:
                    editor_text = editor.get_text()
                    sel_st, sel_end = editor.get_selection()
                    label = os.path.basename(editor_file)
                    if sel_end != sel_st:
                        text = editor_text[sel_st:sel_end]
                    elif editor_text:
                        text = editor_text
        except ImportError:
            pass
    if not text:
        label = 'Clipboard'
        text = clipboard.get().strip()
    if text:
        converted = markdown(text)
        html = TEMPLATE.replace('{{CONTENT}}', converted)

        clip = console.alert('Replace clipboard?', button1='Yes', button2='No', hide_cancel_button=True)
        if clip ==1:
            clipboard.set(html)
            console.hud_alert('HTML copied to clipboard.')
        wv = MyWebView(name='Markdown - %s' % label)
        wv.load_html(html)
        wv.present('full_screen')
    else:
        console.hud_alert('No text found.')
        appex.finish()

if __name__ == '__main__':
    main()
