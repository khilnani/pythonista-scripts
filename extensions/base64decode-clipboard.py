# coding: utf-8
import clipboard, base64, console, appex

etext = clipboard.get()
if 'base64,' in etext:
	etext = etext.split('base64,')[1]
text = base64.decodestring(etext)
try:
	clipboard.set(text)
	if not appex.is_running_extension():
		print text
	console.hud_alert('Clipboard base64 decoded.')
except:
	console.hud_alert('Error base64 decoding clipboard.')