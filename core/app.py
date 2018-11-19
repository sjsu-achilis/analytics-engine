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
from achlib.util.dbutil import db_fetch, db_insup, generate_device_key

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

def get_user_details(userid):
    user_data = templates.get_user_info.copy()
    statement_users = query.get_user_info_1.format(userid)
    log.info("query: {}".format(statement_users))
    result = db_fetch(statement_users)
    if len(result)>0:
        user_data["name"] = result[0][0]
        user_data["email"] = result[0][1]
        user_data["device_key"] = result[0][2]
        user_data["user_present"] = True

    statement_user_info = query.get_user_info_2.format(userid)
    log.info("query: {}".format(statement_user_info))
    result = db_fetch(statement_user_info)
    if len(result)>0:
        user_data["age"], user_data["gender"], user_data["height"], user_data["weight"],\
        user_data["sport_id"],user_data["organization"], user_data["role"] = result[0][0], \
        result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6]

    return user_data


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
    pretty_print_POST(request)
    response = json.loads(request.data)
    for_users_table_vals = "('{}','{}','{}','{}','{}')".format(response["name"],response["email"],response\
                                                   ["userid"],response["password"],generate_device_key())
    statement = query.login_info.format(for_users_table_vals)
    log.info("query: {}".format(statement))
    ok = db_insup(statement)

    return Response(json.dumps({"msg": ok}), headers=HEADER, status=200, mimetype='application/json')


@application.route('/register_user_info', methods=['OPTIONS','POST'])
def register_user_info():
    log.info("/register_user_info")
    pretty_print_POST(request)
    response = json.loads(request.data)
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
    pretty_print_POST(request)
    response = json.loads(request.data)
    uid = response["user_id"]
    val = ""
    for a in response["answers"]:
        val += ",('{}','{}',{},'{}')".format(uid,a["qid"],a["ans"],str(datetime.datetime.now()).split('.')[0])
    log.info("query: {}".format(query.save_response_ins.format(val[1:])))
    ok = db_insup(query.save_response_ins.format(val[1:]))

    return Response(json.dumps({"msg": ok}), headers=HEADER, status=200, mimetype='application/json')


@application.route('/edit_qstn_response', methods=['OPTIONS','POST'])
def edit_qstn_response():
    pretty_print_POST(request)
    log.info("/edit_qstn_response")
    response = json.loads(request.data)
    uid = response["user_id"]
    send_response = []
    for a in response["answers"]:
        statement = query.edit_qstn_response.format(a["ans"],uid,a["qid"])
        log.info("query: {}".format(statement))
        ok = db_insup(statement)
        send_response.append({"qid": a["qid"],"success":ok})

    return Response(json.dumps(send_response), headers=HEADER, status=200, mimetype='application/json')



@application.route('/register_injury', methods=['OPTIONS','POST'])
def register_injury():
    log.info("/register_injury")
    pretty_print_POST(request)
    response = json.loads(request.data)
    if response["date"]:
        date = response["date"]
    else:
        date = str(datetime.datetime.now()).split('.')[0]
    val = "('{}','{}','{}','{}','{}','{}')".format(response["userid"],response["desc"],\
          date,response["type"],response["location"],response["region"])
    statement = query.register_injury.format(val)
    log.info("query: {}".format(statement))
    ok = db_insup(statement)

    return Response(json.dumps({"msg": ok}), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_user_info', methods=['OPTIONS','POST'])
def get_user_info_post():
    log.info('/get_user_info')
    pretty_print_POST(request)
    response = json.loads(request.data)
    statement_validate = query.get_user_info_validate_user.format(response["userid"])
    log.info("query: {}".format(statement_validate))
    result = db_fetch(statement_validate)
    if len(result) == 0:
        return Response(json.dumps({"error": "user not registered"}), headers=HEADER, status=200, mimetype='application/json')
    if result[0][0] != response["password"]:
        return Response(json.dumps({"error": "password invalid"}), headers=HEADER, status=200, mimetype='application/json')
    user_data = get_user_details(response["userid"])

    return Response(json.dumps(user_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/update_user_info', methods=['OPTIONS','POST'])
def update_user_info():
    pretty_print_POST(request)
    log.info("/update_user_info")
    response = json.loads(request.data)
    uid = response["userid"]
    statement_update_users = query.update_user_info_1.format(response["name"],response["email"],uid)
    log.info("query: {}".format(statement_update_users))
    ok_users = db_insup(statement_update_users)

    statement_update_user_info = query.update_user_info_2.format(response["age"],response["gender"],\
                                 response["height"],response["weight"],response["sport_id"],\
                                 response["organization"],response["role"],uid)
    log.info("query: {}".format(statement_update_user_info))
    ok_user_information = db_insup(statement_update_user_info)
    ok = ok_users and ok_user_information

    return Response(json.dumps({"update":ok}), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_user_info', methods=['GET'])
def get_user_info_get():
    log.info('/get_user_info')
    args = request.args.to_dict()["userid"]
    user_data = get_user_details(args)

    return Response(json.dumps(user_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_injury_history', methods=['GET'])
def get_injury_history():
    log.info('/get_injury_history')
    args = request.args.to_dict()["userid"]
    statement = query.get_injury_history.format(args)
    log.info("query: {}".format(statement))
    result = db_fetch(statement)
    send_data = []
    for res in result:
        injury_data = templates.get_injury_data.copy()
        injury_data["desc"],injury_data["date"],injury_data["type"],\
        injury_data["location"],injury_data["region"] = res[1],str(res[2]),res[3],res[4],res[5]
        send_data.append(injury_data)

    return Response(json.dumps(send_data), headers=HEADER, status=200, mimetype='application/json')


@application.route('/register_device_key', methods=['OPTIONS','POST'])
def register_device_key():
    log.info("/register_device_key")
    pretty_print_POST(request)
    response = json.loads(request.data)
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


@application.route('/get_id_from_device_key', methods=['GET'])
def get_id_from_device_key():
    log.info('/get_id_from_device_key')
    args = request.args.to_dict()["device_key"]
    statement = query.get_id_from_device_key.format(args)
    log.info("query: {}".format(statement))
    result = db_fetch(statement)
    send_data = "device_key does not exist"
    if len(result)>0:
        send_data = result[0][0]
    
    return Response(json.dumps({"user_id":send_data}), headers=HEADER, status=200, mimetype='application/json')


@application.route('/get_question_response', methods=['GET'])
def get_question_response():
    log.info('/get_question_response')
    args = request.args.to_dict()["userid"]
    statement = "SELECT qid,question from questionnaire"
    log.info("query: {}".format(statement))
    result = db_fetch(statement)
    lookup = dict(result)
    
    statement = query.get_question_response.format(args)
    log.info("query: {}".format(statement))
    result = db_fetch(statement)

    send_ans = []
    for res in result:
        send_ans.append({"qid": res[0], "qstn":lookup[res[0]], "response":res[1]})
    
    return Response(json.dumps({"user_id":args, "answers":send_ans}), headers=HEADER, status=200, mimetype='application/json')


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
