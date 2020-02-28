import json
import arrow

import gevent
import redis_lock

from gevent import Timeout
from gevent.lock import BoundedSemaphore
from redis import StrictRedis

from exceptions import TooLongTMR
from helpers import timestamp_millisecs, time_elapsed


hits = []

class KeyGen:
    pass

class ResourceManger:
    """
    This is a resource manager that all processes try to get acess to.
    """

    RATE_CALL_LIMIT = 1000  # calls
    RATE_TIME_FRAME = 10 * 60  # 10 minutes
    REDIS_TIMESTAMPS_KEY = 'RESOURCE_API_RATELIMIT'
    REDIS_INDEX_KEY = 'RESOURCE_API_KEY_INDEX'
    key_names, key_sec = ["A", "B", "C"], [0, 1, 2]
    HITS_COUNTER_LOCK = "resource-hits-counter"
    INDEX_COUNTER_LOCK = "resource-key-sec"

    conn = StrictRedis()
    hits_redis_lock = redis_lock.Lock(conn, HITS_COUNTER_LOCK)
    hits_gevent_lock = BoundedSemaphore(1)
    index_redis_lock = redis_lock.Lock(conn, INDEX_COUNTER_LOCK)
    index_gevent_lock = BoundedSemaphore(1)

    @classmethod
    def calculate_waiting_time(cls, hits=None):
        """
        User can defind here its own logic of calculation.
        As defaoult will return just 0
        """

        time_to_sleep = 0
        return time_to_sleep

    @classmethod
    def get_hits_num(cls):
        """ No need to use lock as it's only a 'get'. """
        timestamps_len = cls._get_up_to_date_timestamps()
        return timestamps_len  # integer

    @classmethod
    def _get_up_to_date_timestamps(cls):
        """ Return list of timestamps from Redis.
            Please be aware of the Redis lock when using it! """
        timestamps = hits  # cls.conn.get(cls.REDIS_TIMESTAMPS_KEY)  # returns ordered timestmaps
        # timestamps = [] if timestamps is None else json.loads(timestamps)

        now = timestamp_millisecs()
        ts = timestamps.copy()
        for i in range(len(timestamps)):
            elapsed = time_elapsed(timestamps[i], t0=now)
            if elapsed >= cls.RATE_TIME_FRAME:
                ts.pop(0)
            else:  # stop here, we add new timestamps to the right
                break

        return ts

    @classmethod
    def _set_timestamps(cls, timestamps):
        """ Set list of timestamps on Redis. Please be aware of the Redis lock when using it! """
        global hits
        hits = timestamps

    @classmethod
    def wait_and_increase_tmr(cls, timeout=None):
        """ This method is used directly from WSS. It doesn't return API key-sec as WSS
            doesn't need it like HTTP (it's a constant authenticated connection). """

        if timeout is None:
            print("Warning, timeout not set. using defoult: 200")
            timeout = 200

        try:
            with Timeout(seconds=timeout):
                timestamps = cls._get_up_to_date_timestamps()
                hits_num = len(timestamps)

                # add this call to timestamps
                timestamps += [timestamp_millisecs()]
                cls._set_timestamps(timestamps)

                # wait as much as needed
                wait_time = cls.calculate_waiting_time(hits_num)
                gevent.sleep(wait_time)
                return

        except Timeout:
            raise TooLongTMR(f'I have been waiting {timeout} seconds for TMR bumber!')

    @classmethod
    def get_key_sec(cls):

        # this blocks until key is retreived
        timeout = 3
        gotit_rlock = False
        gotit_glock = False
        try_num = 2
        for i in range(try_num):
            try:
                with Timeout(seconds=timeout):
                    # wait for in-process lock between all coros
                    cls.index_gevent_lock.acquire()
                    gotit_glock = True

                    # wait for inter-process Redis lock between all processes
                    cls.index_redis_lock.acquire()
                    gotit_rlock = False
                    # get next key
                    key_index = cls.conn.get(cls.REDIS_INDEX_KEY)
                    key_index = json.loads(key_index) if key_index else -1

                    new_key_idx = key_index + 1
                    if new_key_idx >= len(cls.key_names):
                        new_key_idx = 0

                    cls.conn.set(cls.REDIS_INDEX_KEY, new_key_idx)

                    key_sec = cls.key_sec[cls.key_names[new_key_idx]]
                    return key_sec['key'], key_sec['sec']

            except Timeout as e:
                if i == try_num -1:
                    raise TooLongTMR(f'timeout: {timeout}')

            finally:
                try:
                    if gotit_rlock:
                        cls.index_redis_lock.release()
                    else:
                        pass
                except redis_lock.NotAcquired:
                    pass

                try:
                    if gotit_glock:
                        cls.index_gevent_lock.release()
                    else:
                        pass

                except (RuntimeError, ValueError) as e:
                    if "cannot release un-acquired lock" not in str(e):
                        raise e  # unknown error

                gevent.sleep(0)

    @classmethod
    def print_hits_counter(cls):
        while True:
            print(cls.get_hits_num())
            gevent.sleep(1)
