# coding: utf-8

import appex, clipboard, console
from markdown2 import markdown
import ui, scene

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
	text = ''
	if appex.is_running_extension():
		text = appex.get_text()
	if not text:
		console.hud_alert('Using clipboard.')
		text = clipboard.get().strip()
	if text:
		converted = markdown(text)
		html = TEMPLATE.replace('{{CONTENT}}', converted)
		
		clip = console.alert('Copy to clipboard?', button1='Yes', button2='No', hide_cancel_button=True)
		if clip ==1:
			clipboard.set(html)
			console.hud_alert('HTML copied to clipboard.')
		wv = MyWebView(name='Markdown Preview')
		wv.load_html(html)
		wv.present('full_screen')
	else:
		console.hud_alert('No text found.')
		appex.finish()

if __name__ == '__main__':
	main()