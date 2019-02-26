"""
This is a basic version which works fine but has several drawbacks. The biggets of them is that it needs access to local file system.
In many occasions, this isn't possible (e.g. when running in the cloud)
"""

import random
import time
import arrow
import gevent
import sys


def get_flock(fname):
    """ acquire flock, add ts to file and return when ts is first line. """
    ts = str(arrow.utcnow().timestamp)

    with open(fname, 'a') as f:
        f.write(f"{ts}\n")

    while True:
        with open(fname, 'r') as f:
            lines = f.readlines()
            lines = [line.strip('\n') for line in lines]
            if ts == lines[0]:
                myprint(f'{sys.argv[1]} in')
                return ts
            assert ts in str(lines)  # solution: add yourself again
        gevent.sleep(0.1)


def remove_flock(fname, ts):
    with open(fname, 'r') as f:
        lines = f.readlines()

    # filter out my ts
    new_lines = [line for line in lines if str(ts) != line.strip('\n')]
    with open(fname, 'w+') as f:
        f.writelines(new_lines)

    myprint(f'{sys.argv[1]} out')
    return len(new_lines) < len(lines)


fname = 'lock1'
logfile = 'locklog'


def myprint(msg):
    with open(logfile, 'a+') as f:
        f.writelines([msg+'\n'])


def coro(x):
    while True:
        key_generator.APIKeyGenerator.wait_and_increase_tmr()
        myprint(f'{x} is happy -{len(key_generator.hits)}')
        gevent.sleep(random.random())


coros = [gevent.spawn(coro, i) for i in range(int(sys.argv[1]))]
gevent.joinall(coros)
