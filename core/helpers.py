# -*- coding: utf-8 -*-
import query
import templates
import csv
import random
import math

from achlib.config import file_config
from achlib.util import logger
from achlib.util.dbutil import db_fetch, db_insup, generate_device_key

config = file_config()
log = logger.getLogger(__name__)

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
    user_data["userid"] = userid
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

    
def convert_float(val,scale):
    if '.' in val:
        return str(math.ceil(float(val)*1000*scale))
    return str(math.ceil(float(val)*scale))


def insert_user_health_stats(userid=None, do_scale=False):
    f = open('One_Year_of_FitBitChargeHR_Data.csv', 'rb')
    reader = csv.reader(f)
    q = "insert into health_metrics values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
    for i,row in enumerate(reader):
        scale = 1.0
        if i==0:
            continue
        if do_scale:
            scale = random.uniform(0.5,1.0)

        date = '-'.join([row[0].split('-')[1],row[0].split('-')[0],row[0].split('-')[2]])
        calorie,steps,dist,floors,m_sitting,m_slow,m_mod,m_int,cal_act = convert_float(row[1],scale),\
        convert_float(row[2],scale),convert_float('.'.join(row[3].split(',')),scale),convert_float(row[4],scale),\
        convert_float(row[5],scale),convert_float(row[6],scale),convert_float(row[7],scale),convert_float(row[8],scale),\
        convert_float(row[9],scale)
        
        statement = q.format(date,userid,calorie,steps,floors,dist,m_sitting,m_slow,m_mod,m_int,cal_act)
        log.info("query: {}".format(statement))
        ok = db_insup(statement)
        log.info("row {}: {}".format(i,ok))

