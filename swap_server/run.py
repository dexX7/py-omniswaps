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

    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger('werkzeug')
    logger.addHandler(handler)

    app.logger.addHandler(handler)
    app.run(debug=True, port=5000)
