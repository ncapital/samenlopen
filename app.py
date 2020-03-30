#!/usr/bin/env python
from flask import Flask
from views import controller_bp

controller = Flask(__name__)
controller.register_blueprint(controller_bp)
controller.run(host='::', port=5000, use_reloader=True)
