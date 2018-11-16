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


@application.route('/get_sports', methods=['GET'])
def get_sports():
    log.info('/get_sports')
    statement = query.get_sports
    result = db_fetch(statement)
    send_data = []
    for r in result:
        send_data.append(collections.OrderedDict({u"s_id": r[0], u"s_nsme": r[1], u"s_type":r[2]}))

    return Response(json.dumps(send_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/is_uid_available', methods=['GET'])
def is_uid_available():
    log.info('/is_uid_available')
    args = (request.args.to_dict()["userid"],)
    statement = query.is_uid_available
    result = set(db_fetch(statement))
    send_data = {"avl": args not in result}

    return Response(json.dumps(send_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/login_info', methods=['OPTIONS','POST'])
def login_info():
    log.info('/login_info')
    response = request.json
    for_users_table_vals = "('{}','{}','{}','{}')".format(response["name"],response["email"],response\
                                                   ["userid"],response["password"])
    statement = query.login_info.format(for_users_table_vals)
    log.info("query: {}".format(statement))
    ok = db_insup(statement)

    return Response(json.dumps({"msg": ok}), headers=HEADER, status=200, mimetype='application/json')


@application.route('/register_user_info', methods=['OPTIONS','POST'])
def register_user_info():
    log.info("/register_user_info")
    response = request.json
    for_users_info_table_vals = "('{}',{},'{}',{},{},'{}','{}',{})".\
                                format(response["userid"],response["age"],\
                                response["gender"],response["height"],response["weight"],\
                                response["s_id"],response["org"],response["role"])
    statement = query.register_user_info.format(for_users_info_table_vals)
    log.info("query: {}".format(statement))
    ok = db_insup(statement)

    return Response(json.dumps({"register": ok}), headers=HEADER, status=200, mimetype='application/json')


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


@application.route('/edit_qstn_response', methods=['OPTIONS','POST'])
def edit_qstn_response():
    log.info("/edit_qstn_response")
    response = request.json
    uid = response["user_id"]
    send_response = []
    for a in response["answers"]:
        statement = query.edit_qstn_response.format(a["ans"],uid,a["qid"])
        log.info("query: {}".format(statement))
        ok = db_insup(statement)
        send_response.append({"qid": a["qid"],"success":ok})

    return Response(json.dumps(send_response), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_injury_history', methods=['GET'])
def get_injury_history():
    log.info('/get_injury_history')
    args = request.args.to_dict()["userid"]
    statement = query.get_injury_history.format(args)
    log.info("query: {}".format(statement))
    result = db_fetch(statement)
    send_data = []
    for res in result:
        injury_data = templates.get_injury_data
        injury_data["desc"],injury_data["date"],injury_data["type"],\
        injury_data["location"],injury_data["region"] = res[1],str(res[2]),res[3],res[4],res[5]
        send_data.append(injury_data)

    return Response(json.dumps(send_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/register_device_key', methods=['OPTIONS','POST'])
def register_device_key():
    log.info("/register_device_key")
    response = request.json
    statement = query.register_device_key.format(response["device_key"],response["user_id"])
    log.info("query: {}".format(statement))
    ok = db_insup(statement)

    return Response(json.dumps({"msg": ok}), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_device_key', methods=['GET'])
def get_device_key():
    log.info('/get_device_key')
    args = request.args.to_dict()["userid"]
    statement = query.get_device_key.format(args)
    log.info("query: {}".format(statement))
    result = db_fetch(statement)

    return Response(json.dumps({"device_key":result[0][0]}), headers=HEADER, status=200, mimetype='application/json')


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
