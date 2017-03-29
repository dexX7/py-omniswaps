#!/usr/bin/env python
import logging
from logging.handlers import RotatingFileHandler
from app import app

if __name__ == "__main__":
    formatter = logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
''')

    handler = RotatingFileHandler('logs/flask.log', maxBytes=1000000, backupCount=50)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger('werkzeug')
    logger.addHandler(handler)

    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=5000)
