# SuperFastPython.com
# example of a long-running daemon thread
from time import sleep
from random import random
from threading import Thread
 
# long-running background task
def background_task():
    global data
    # record the last seen value
    last_seen = data
    # run forever
    while True:
        # check for change
        if data != last_seen:
            # report the change
            print(f'Monitor: data has changed to {data}')
            # update last seen
            last_seen = data
        # block for a while
        sleep(0.1)
 
# global data
data =  0
# create and start the daemon thread
print('Starting background task...')
daemon = Thread(target=background_task, daemon=True, name='Monitor')
daemon.start()
# main thread is carrying on...
print('Main thread is carrying on...')
for _ in range(5):
    # block for a while
    value = random() * 5
    sleep(value)
    # update the data variable
    data = value
print('Main thread done.')