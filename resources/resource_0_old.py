"""
Here we define the resource and its attributes.
The one thing that must be defined is the __next__ method
Any sleep times must be sent up to caller and not implemented at this level!
"""
import gevent
import time
from exceptions import TimeOut
from helpers import get_keys_and_secrets, time_elapsed


class KeyGen:
    resource_name = 'resource_0'
    key_names, key_sec = get_keys_and_secrets(resource_name)

    def __init__(self):
        """ create default timestamp per key for all keys stored at
            self.key_names
        """
        self.timestamp_per_key = {key: time.time() for key in self.key_names}

    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        """
        increase self.a value by 1, but return the old value.
        """
        self.a += 1
        return self.a - 1

    def get_key_sec(self, timeout=5):
        """
        :return: (key, secret) if found available,
                             else: raise exception

        The main constrains of the current resource of "using the keys" are implemented here.
        - at this example, the constrain is "using 1 key for no more than once a sec".
        """

        t0 = time.time()
        while time.time() - t0 < timeout:
            for keyname in self.timestamp_per_key:
                last_ts = self.timestamp_per_key[keyname]
                if time.time() - last_ts > 1:
                    # found key w/o usage in the past 1 sec.
                    self.timestamp_per_key[keyname] = time.time()
                    return self.key_sec[keyname]['key'], self.key_sec[keyname]['sec'], 0

            gevent.sleep(0.05)

        raise TimeOut(f"Couldn't get available key:sec for "
                      f"resource: {self.resource_name} with timeout: {timeout}")
