import editor, ui

text = editor.get_text()
if not text:
    sys.exit('No text in the Editor.')

wv = ui.WebView()
wv.present('sheet')
wv.load_url(editor.get_path())
