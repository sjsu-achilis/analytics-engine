# -*- coding: utf-8 -*-
import os
import sys

import requests
from flask import Flask, request, Response
import pprint
import json

import query
import templates
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


@application.route('/get_metric', methods=['GET'])
def get_metric(*args, **kwargs):
    '''
    userid, start_timestamp, end_timestamp, metric_label
    '''
    pretty_print_POST(request)
    args = request.args.to_dict()
    send_data = {
      u"values": []
      }

    statement = query.get_metric.format(str(args['userid']),args\
                ['metric_label'],args['start_timestamp'],args['end_timestamp'])

    log.info('query:  {}'.format(statement))
    result = db_fetch(statement)
    log.info(result)
    for res in result:
        temp = templates.get_metric.copy()
        if res[0]:
            temp["event_timestamp"] = str(res[0])
        if res[1]:
            temp["metric_value"] = str(res[1])
        send_data["values"].append(temp)
    log.info("sent response \n{}".format(pprint.pformat(send_data)))

    return Response(json.dumps(send_data), status=200, mimetype='application/json')


@application.route('/get_max_metric', methods=['GET'])
def get_max_metric(*args, **kwargs):
    '''
    userid, start_timestamp, end_timestamp, metric_label
    '''
    pretty_print_POST(request)
    args = request.args.to_dict()
    send_data = {
      u"values": []
      }

    statement = query.get_max_metric.format(str(args['userid']),args\
                ['metric_label'],args['start_timestamp'],args['end_timestamp'])

    log.info('query:  {}'.format(statement))
    result = db_fetch(statement)
    log.info(result)
    for res in result:
        temp = templates.get_max_metric.copy()
        if res[0]:
            temp["event_timestamp"] = str(res[0])
        if res[1]:
            temp["max_metric_value"] = str(res[1])
        send_data["values"].append(temp)
    log.info("sent response \n{}".format(pprint.pformat(send_data)))

    return Response(json.dumps(send_data), status=200, mimetype='application/json')



def pretty_print_POST(req):
    """
    This method takes a request and print
    """
    log.info('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        '\n'.join('{}: {}'.format(k, v) for k, v in req.args.to_dict().items()),
    ))


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
