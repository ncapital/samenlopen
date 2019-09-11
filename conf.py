class BaseConfig:
    sleep_options = {'server', 'client'}  # where would waiting time take place


class Sleep:
    SERVER = 'server'
    CLIENT = 'client'
    options = [SERVER, CLIENT]
