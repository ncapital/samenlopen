import json

# import gevent

from flask import Blueprint, request, abort

# from common import ResourceHandler
from conf import BaseConfig, Sleep
from exceptions import *

controller_bp = Blueprint(__name__, "samenlopen", url_prefix='')


@controller_bp.route('/<string:resource>', methods=['GET'])
def fetch(resource):
    # validate sleep location
    sleep_location = request.args.get('sleep')
    if sleep_location not in Sleep.options:
        abort(400, f"Client must specify where to sleep! options: {BaseConfig.sleep_options}")

    return 'yo'

    # try:
    #     keygen = ResourceHandler.get_resource_handler(resource)
    # except UnknownResource as e:
    #     abort(404, str(e))
    #
    # key, secret, sleep_time = keygen.get_key_sec()
    # if sleep_location == Sleep.SERVER:
    #     gevent.sleep(sleep_time)
    #     res = {}
    #     res.update({'key': key})
    #     res.update({'secret': secret})
    #     res.update({'sleep': 0})
    #     return json.dumps(res)
    #
    # elif sleep_location == Sleep.CLIENT:
    #     return key, secret, sleep_time
    #
    # else:
    #     print(f"Unsupported sleep mode! {sleep_location}")
    #     abort(500)
