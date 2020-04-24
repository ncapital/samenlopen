import arrow
import datetime
import gevent
import redis_lock


from redis import StrictRedis
from helpers import time_elapsed, timestamp_millisecs
from utils.loaders import load_keys


class Bit2c:
    def __init__(self, yaml_config_file):
        self.keys = load_keys(yaml_config_file)


class KeyGen:
    """
    All keys on all machines should be matching numbers to keys.
    You can have key 0-5 on machine A and 3-9 on another as long
    as key3 is the same on both and so on
    """

    keys = Bit2c('resources/r0.yaml')
    conn = StrictRedis()

    @classmethod
    def get_key_sec(cls):
        # this blocks until key is retreived TODO add timeout?
        with redis_lock.Lock(cls.conn, "bit2c", expire=3600, auto_renewal=True):
        #with cls.glock:
            timestamps = cls.conn.mget(cls.key_names)  # returns ordered timestmaps

            # keep checking for 5 secs
            now = arrow.utcnow().timestamp
            while arrow.utcnow().timestamp - now < 5:
                for idx, ts in enumerate(timestamps):
                    if ts is None or time_elapsed(ts) > 0.9:
                        key = cls.key_names[idx]
                        # set timestamp_millisecs for this key (expire in 1 sec)
                        cls.conn.set(key, timestamp_millisecs(), ex=1)
                        return cls.key_sec[key]['key'], cls.key_sec[key]['sec']

                gevent.sleep(0.2)

            raise Exception(f"Bit2c: Couldn't get key:sec!")
