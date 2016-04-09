# coding: utf-8
import clipboard, base64, console, appex

text = clipboard.get()
etext = base64.encodestring(text)
etext = 'data:text/html;base64,' + etext
try:
	clipboard.set(etext)
	if not appex.is_running_extension():
		print etext
	console.hud_alert('Clipboard base64 encoded.')
except:
	console.hud_alert('Error base64 encoded clipboard.')