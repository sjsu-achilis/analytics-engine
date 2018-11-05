# -*- coding: utf-8 -*-
import os
import sys
import collections
import datetime

import requests
from flask import Flask, request, Response
from flask_cors import CORS
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
CORS(application)

HEADER = {'Access-Control-Allow-Origin': '*'}

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


@application.route('/', methods=['GET'])
def verify():
    log.info('service health')
    return 'service is up'


@application.route('/get_metric', methods=['GET'])
def get_metric(*args, **kwargs):
    '''
    userid, start_timestamp, end_timestamp, metric_label
    '''
    log.info("/get_metric")
    args = request.args.to_dict()
    statement = query.get_metric.format(str(args['userid']),args\
                ['metric_label'],args['start_timestamp'],args['end_timestamp'])

    send_data = {
      u"label": args['metric_label'],
      u"values": []
      }
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

    return Response(json.dumps(send_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_max_metric', methods=['GET'])
def get_max_metric(*args, **kwargs):
    '''
    userid, start_timestamp, end_timestamp, metric_label
    '''
    log.info("/get_max_metric")
    args = request.args.to_dict()
    statement = query.get_max_metric.format(str(args['userid']),args\
                ['metric_label'],args['start_timestamp'],args['end_timestamp'])

    send_data = {
      u"label": args['metric_label'],
      u"values": []
      }
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

    return Response(json.dumps(send_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_questions', methods=['GET'])
def get_questions():
    log.info("/get_questions")
    statement = query.get_questions
    result = db_fetch(statement)
    send_data = []
    for r in result:
        send_data.append(collections.OrderedDict({u"q_id": r[0], u"qst": r[1]}))

    return Response(json.dumps(send_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/save_response', methods=['OPTIONS','POST'])
def save_response():
    log.info("/save_response")
    response = request.json
    uid = response["user_id"]
    val = ""
    for a in response["answers"]:
        val += ",('{}','{}',{},'{}')".format(uid,a["qid"],a["ans"],str(datetime.datetime.now()).split('.')[0])
    log.info("query: {}".format(query.save_response_ins.format(val[1:])))
    ok = db_insup(query.save_response_ins.format(val[1:]))
    
    return Response(json.dumps({"msg": ok}), headers=HEADER, status=200, mimetype='application/json')


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
