#!/usr/bin/env python

# import sys
from flask import Flask
from views import controller_bp
from common import keygens

app = Flask(__name__)
# print(sys.argv)
#
# for arg in sys.argv[1:]:
#     # load keys/secrets
#     pass

import IPython
# IPython.embed(colors='neutral')
IPython.embed()

app.register_blueprint(controller_bp)
app.run(host='::', port=5000, use_reloader=True, load_dotenv=True)
