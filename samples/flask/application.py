# coding: utf-8
from flask import Flask, request, render_template
import socket
app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello World!'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
		return render_template('hello.html', name=name)


# Attempt at getting this device's ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.google.com', 9))
print 'My IP: ' + s.getsockname()[0]
s.close()

print('Navigate to: http://localhost:5000/hello/nik')
app.run(host='0.0.0.0')
