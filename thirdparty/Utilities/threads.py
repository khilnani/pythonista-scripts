# coding: utf-8
import threading
import time
abort=False
def ping():
    while not abort:
        print('I am thread number 1')
        time.sleep(5)
def pong():
    while not abort:
        print('I am thread number 2')
        time.sleep(5)

threading.Thread(target=ping).start()
threading.Thread(target=pong).start()