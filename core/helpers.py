# -*- coding: utf-8 -*-
import query
import templates
import csv
import random
import math
import datetime
import collections
from datetime import timedelta, date

from achlib.config import file_config
from achlib.util import logger
from achlib.util.dbutil import db_fetch, db_insup, generate_device_key, generate_session_id

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


def daterange(date1, date2):
    ret = []
    for n in range(int ((date2 - date1).days)+1):
        ret.append((date1 + timedelta(n)).strftime("%Y-%m-%d"))

    return ret
    

def session_data_list(start_dt,end_dt,userid,w_size):
    dates = daterange(start_dt,end_dt)
    up_list = []
    lamb = float(2)/(w_size+1)
    for i,d in enumerate(dates):
        # on-season training data
        rpe = 0
        if 1<=int(d.split('-')[1])<=3:
            duration,rating = random.randint(45,75),random.randint(2,5)
            rpe = duration*rating
        if 4<=int(d.split('-')[1])<=6:
            duration,rating = random.randint(60,90),random.randint(5,7)
            rpe = duration*rating
        if 7<=int(d.split('-')[1])<=9:
            duration,rating = random.randint(90,120),random.randint(8,10)
            rpe = duration*rating
        if 10<=int(d.split('-')[1])<=12:
            duration,rating = random.randint(60,90),random.randint(4,6)
            rpe = duration*rating

        #calculate ctl
        sum_ = rpe
        for w in up_list[::-1][:20]:
            sum_ += w[-1]
        ctl = sum_/(len(up_list[::-1][0:20])+1)
        # calculate atl
        sum_ = rpe
        for w in up_list[::-1][:6]:
            sum_ += w[-1]
        atl = sum_/(len(up_list[::-1][0:7])+1)
        # calculate awcr
        if ctl != 0:
            acwr = atl/ctl
        else:
            acwr = 0
        #calculate EWMA
        if i==0:
            ewma = acwr
        else:
            ewma = (rpe * lamb) + ((1-lamb)*up_list[-1][-1])

        up_list.append([d,userid,None,None,duration,rating,rpe,ctl,atl,ctl-atl,acwr,ewma])


    return up_list


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


def generate_session_data():
    users = ['2134225533','1342252213','1673662323','9978656676','1414252511']
    f = open('session_data.csv','w+')
    writer = csv.writer(f)
    writer.writerow(['date','userid','start_timestamp','end_timestamp',\
    'duration','rating','rpe','ctl','atl','tsb','acwr','ewma'])
    for user in users:
        start_dt = date(2015, 5, 8)
    	end_dt = date(2016, 5, 7)
        for row in session_data_list(start_dt,end_dt,user,7):
            writer.writerow(row)


def insert_session_data():
    f = open('session_data.csv', 'rb')
    reader = csv.reader(f)
    q = "insert into sessions values ({},'{}','{}',NULL,NULL,'{}','{}','{}','{}','{}','{}','{}','{}')"
    for i,row in enumerate(reader):
        if i==0:
            continue
        statement = q.format(generate_session_id(),row[0],row[1],row[4],row[5],row[6],row[7],row[8],row[9],\
        row[10],row[11])
        log.info("query: {}".format(statement))
        ok = db_insup(statement)
        log.info("row {}: {}".format(i,ok))

def generate_session_answers():
    f = open('session_answers.csv','w+')
    writer = csv.writer(f)
    for i in range(1830):
        for j in range(6):
            writer.writerow([i+1,j+1,random.randint(5,10)])
        

if __name__ == "__main__":
    generate_session_answers()

