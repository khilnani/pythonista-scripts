# coding: utf-8

import socket
import appex, console, clipboard

if appex.is_running_extension():
    if appex.get_url():
        hostname = appex.get_url()
    else:
        hostname = appex.get_text()
else:
    hostname = console.input_alert('Hostname')

if hostname:
    try:
        addr = socket.gethostbyname(hostname)
        console.input_alert('IP Address', hostname, addr)
    except Exception as e:
        console.alert(str(e))
else:
    console.alert('No hostname provided')
