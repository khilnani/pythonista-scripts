# coding: utf-8
import clipboard, datetime, console, appex

if appex.is_running_extension():
	text = appex.get_text()
else:
	text = clipboard.get()
filename = '{:%Y%m%d-%H%M%S}-clip.txt'.format(datetime.datetime.now())
with open(filename, 'w') as f:
	f.write(text)
console.hud_alert('Saved to: ' + filename)
if appex.is_running_extension():
	appex.finish()
