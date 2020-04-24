#!/usr/bin/env python

# import sys
import argparse

import common

from flask import Flask
from views import controller_bp
from resources import r0


# parse input args to know which resources to expose
parser = argparse.ArgumentParser(description='Samenloop')
parser.add_argument("--r0", action="store_true")
parser.add_argument("--r1", action="store_true")
args = parser.parse_args()


if args.r0:
    common.RESOURCE_MAP[common.Resources.RESOURCE_0] = r0
if args.r1:
    common.RESOURCE_MAP[common.Resources.RESOURCE_1] = r0  # todo change to r1

import IPython
# IPython.embed(colors='neutral')
# IPython.embed()

app = Flask(__name__)
app.register_blueprint(controller_bp)
app.run(host='::', port=5000, use_reloader=True, load_dotenv=True)
