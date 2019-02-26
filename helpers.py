import arrow
import datetime
import os
import re
import subprocess

from datetime import timedelta
from logging import warning


def colorize(s, color):
    class Color:
        YELLOW = '\033[1;33m'
        RED = '\033[1;91m'
        GREEN = '\033[1;92m'
        GREY_BG = '\033[37;100m'
        NO_COLOR = '\033[0m'

    color = color.upper()
    if not hasattr(Color, color):
        warning(f"Unknown color! ({color})")
        return s

    return f"{getattr(Color, color)}{s}{Color.NO_COLOR}"


def yellow(s):
    return colorize(s, 'YELLOW')


def red(s):
    return colorize(s, 'RED')


def green(s):
    return colorize(s, 'GREEN')


def grey_bg(s):
    return colorize(s, 'GREY_BG')


def print_full_width(s, color=None):
    std_out_width = os.get_terminal_size().columns
    spaces = int(std_out_width/2 - len(s)/2) * ' '
    msg = spaces + s + spaces
    if color:
        msg = colorize(msg, color)
    print(msg)


def is_port_taken(port):
    output = subprocess.check_output(["netstat", "-antu"])
    return f'::{port}' in output.decode('utf-8')


def timestamp_millisecs():
    return round(arrow.utcnow().float_timestamp, 3)


def get_env_vars(pattern):
    """ Return a list of all keys matching pattern 'regex'. """
    res = list()
    for var in os.environ:
        if regex_matches(pattern, var):
            res += [var]

    return res


def regex_matches(pattern, text):
    return bool(re.match(pattern, text))


def get_keys_and_secrets(ex_name):
    """ Return list of names for all keys found for ex
        and also a dict {key_nam: {'key':<KEY>, 'sec': <SECRET>}} for a given ex name. """

    env_var_regex = f"^{ex_name.upper()}_KEY_[0-9]*$"
    key_names = get_env_vars(env_var_regex)

    if not key_names:
        raise Exception(f"{ex_name}: No key:sec found as env vars!")

    key_names.sort()
    print(f"{ex_name}: Using {len(key_names)} keys.")

    key_sec = dict()
    for key_name in key_names:
        key = os.getenv(key_name)
        sec = os.getenv(key_name.replace('KEY', 'SECRET'))
        if not sec:
            raise Exception(f"Key has no secret! {key_name}")

        key_sec[key_name] = {'key': key}
        key_sec[key_name]['sec'] = sec

    return key_names, key_sec


def time_elapsed(timestamp, t0=None):
    """ Return time (in milliseconds) since timestamp. """
    if isinstance(timestamp, bytes):
        timestamp = float(timestamp)

    if isinstance(timestamp, datetime.datetime):
        timestamp = arrow.get(timestamp).float_timestamp

    if t0 is None:
        t0 = timestamp_millisecs()

    diff = t0 - timestamp
    assert diff >= 0, f"timestamp is in the future! ({timestamp})"
    return diff


def utc_nonce():
    """ Return an ever increasing timestamp string with 5 digits after the decimal point. """
    float_nonce = arrow.utcnow().float_timestamp
    return '{:.5f}'.format(float_nonce).replace('.', '')


def a_year_ago_datetime():
    return arrow.utcnow().datetime - timedelta(weeks=52)


def _plog(msg, screen_header=None, log_header=None, log_fname=None):

    if screen_header:
        print(f"{screen_header}: {msg}")

    if log_header:
        with open(log_fname, "a") as f:
            f.write(f"[{arrow.utcnow().float_timestamp}]{log_header}: {msg}\n")

    if not screen_header and not log_header:
        print(msg)
