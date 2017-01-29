# coding: utf-8
"""
Description:
- Starts up a simple HTTP server with the open file's directory as the Document Root.

Instructions:
- Add the script to the Pythonista Actions Shortcut menu.
- Open any file in the directory you want the server to start, and run the script.
"""
import SimpleHTTPServer
import BaseHTTPServer
import socket
import os

PORT = 8000

try:
    import editor
    file = editor.get_path()
    dir = os.path.sep.join( file.split( os.path.sep )[:-1] )
    print('Using dir: %s' % dir)
    os.chdir( dir )
except ImportError:
    print('Not run in iOS Pythonista, will use current working directory')

try:
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = BaseHTTPServer.HTTPServer(('', PORT), Handler)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip = s.getsockname()[0]
    s.close()
    
    print("Server started at: http://%s:%s" % (ip, PORT))
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Shutting down ...")
    httpd.shutdown()
    httpd.socket.close()
    httpd.server_close()
    print("Done.")
    
