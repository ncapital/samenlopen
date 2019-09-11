"""
Here we define the resource and its attributes.
The one thing that must be defined is the __next__ method
Any sleep times must be sent up to caller and not implemented at this level!
"""
import gevent
import time

from helpers import get_keys_and_secrets, time_elapsed


class KeyGen:
    key_names, key_sec = get_keys_and_secrets('resource_0')

    def __init__(self):
        self.timestamp_per_key = {key: time.time() for key in self.key_names}

    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x

    def get_key_sec(self):
        # keep checking for 5 secs
        t0 = time.time()
        while time.time() - t0 < 5:
            for keyname in self.timestamp_per_key:
                ts = self.timestamp_per_key[keyname]
                if time.time() - ts > 1:
                    self.timestamp_per_key[keyname] = time.time()
                    return self.key_sec[keyname]['key'], self.key_sec[keyname]['sec'], 0

            gevent.sleep(0.05)

        raise Exception(f"Couldn't get key:sec!")
