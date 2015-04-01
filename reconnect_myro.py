from remotebot import configuration
import os
import time

# Free rfcomms
for i in range(20):
    if os.path.exists('/dev/rfcomm{}'.format(i)):
        os.system('fuser /dev/rfcomm{} | cut -d: -f2 | xargs kill'.format(i))
        os.system('rfcomm release rfcomm{}'.format(i))
        time.sleep(1)
        os.system('rfcomm release rfcomm{}'.format(i))

scribblers = 0

for model, ids in configuration.robots.items():
    if model == 'scribbler':
        for id_ in ids:
            print('rfcomm bind rfcomm{} {} 1'.format(scribblers, id_))
            os.system('rfcomm bind rfcomm{} {} 1'.format(scribblers, id_))
            scribblers += 1
