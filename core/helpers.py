# -*- coding: utf-8 -*-
import query
import templates
import csv

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

    
def insert_user_health_stats(userid=None):
    f = open('One_Year_of_FitBitChargeHR_Data.csv', 'rb')
    reader = csv.reader(f)
    q = "insert into health_metrics values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
    for i,row in enumerate(reader):
        if i==0:
            continue
        replace = '.'.join(row[3].split(','))
        date = '-'.join([row[0].split('-')[1],row[0].split('-')[0],row[0].split('-')[2]])
        statement = q.format(date,userid,row[1],row[2],replace,row[4],row[5],row[6],row[7],row[8],row[9])
        log.info("query: {}".format(statement))
        ok = db_insup(statement)
        log.info("row {}: {}".format(i,ok))

    