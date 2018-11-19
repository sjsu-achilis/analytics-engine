# -*- coding: utf-8 -*-
get_metric = "select event_timestamp, metric_value from \
health_metrics where userid='{}' and metric_label='{}' \
and event_timestamp::date between '{}' and '{}'"

get_max_metric = "select event_timestamp, max(metric_value) from \
health_metrics where userid='{}' and metric_label='{}' \
and event_timestamp::date between '{}' and '{}' group by event_timestamp"

get_questions = "select * from questionnaire"

save_response_ins = "insert into questionnaire_response values {}"

edit_qstn_response = "update questionnaire_response set response={} \
where userid='{}' and qid='{}'"

get_sports = "select * from sports"

is_uid_available = "select userid from users"

login_info = "insert into users values {}"

register_user_info = "insert into user_information values {}"

get_injury_history = "select * from injury_history where userid='{}'"

register_device_key = "update users set device_key='{}' where userid='{}'"

get_device_key = "select device_key from users where userid='{}'"

register_injury = "insert into injury_history values {}"

get_user_info_validate_user = "select password from users where userid = '{}'"

get_user_info_1 = "select name,email,device_key from users where userid = '{}'"

get_user_info_2 = "select age,gender,height,weight,sport_id,organization,role from \
user_information where userid = '{}'"

get_user_info_3 = "select name from sports where id = '{}'"

get_id_from_device_key = "select userid from users where device_key = '{}'"

update_user_info_1 = "update users set name='{}',email='{}' where userid='{}'"

update_user_info_2 = "update user_information set age={},gender='{}',height={},weight={},\
sport_id='{}',organization='{}',role={} where userid='{}'"

get_question_response = "select qid,response from questionnaire_response where userid='{}'"