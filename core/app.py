# -*- coding: utf-8 -*-
import os
import sys

import requests
from flask import Flask, request, Response
import pprint

from achlib.config import file_config
from achlib.util import logger
from achlib.util.dbutil import db_fetch, db_insup

config = file_config()
log = logger.getLogger(__name__)

application = Flask(__name__)

@application.route('/', methods=['GET'])
def verify():
    log.info('service health')
    return 'service is up'


#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
