# -*- coding: utf-8 -*-
get_metric = "select event_timestamp, metric_value from \
health_metrics where userid='{}' and metric_label='{}' \
and event_timestamp::date between '{}' and '{}'"

get_max_metric = "select event_timestamp, max(metric_value) from \
health_metrics where userid='{}' and metric_label='{}' \
and event_timestamp::date between '{}' and '{}' group by event_timestamp"

get_questions = "select * from questionnaire"

save_response_ins = "insert into questionnaire_response values {}"

edit_qstn_response = "update questionnaire_response set response='{}' \
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

post_event = "insert into event values {}"

get_event = "select event_start_ts,event_end_ts,event_description,title from event where userid='{}'"

register_app_instance = "insert into app_tokens values ('{}','{}')"

register_coach_student = "insert into athlete_relations values ('{}','{}','{}',{})"

get_coach_types = "select * from coach_type"

get_athelete_ids1 = "select organization from user_information where userid = '{}'"

get_athelete_ids2 = "select distinct ui.userid, u.name from user_information ui inner join \
users u on ui.userid=u.userid where ui.organization='{}'"

get_athletes_for_coach = "select u.userid, u.name from athlete_relations ar inner join users \
u on ar.athlete_id=u.userid where ar.coach_id='{}'"

get_daily_health_data = "select * from health_metrics where event_timestamp between '{}' and '{}' and userid = '{}'"

add_day_data_check_rows = "select 1 from health_metrics where event_timestamp = '{}' and userid = '{}'"

add_day_data_add_row = "insert into health_metrics values ('{}','{}')"

add_day_data_set_value_once = "update health_metrics set {}='{}' where event_timestamp = '{}' and userid = '{}'"

add_day_data_fetch_value = "select {} from health_metrics where event_timestamp = '{}' and userid = '{}'"

get_session_questions = "select id, question from session_questions"

register_session_info1 = "insert into sessions values ({},'{}','{}','{}','{}','{}')"

register_session_info2 = "update sessions set rating = {} where id = {}"

register_session_info3 = "insert into session_answers values ({},{},{})"

get_session_info1 = "select * from sessions where date between '{}' and '{}' and userid = '{}'"

get_session_info2 = "select * from session_answers where session_id in {}"

update_session_info1 = "update sessions set start_timestamp='{}', end_timestamp='{}', duration='{}', rating = '{}' \
where id={}"

update_session_info2 = "update session_answers set response='{}' where session_id='{}' and qid='{}'"

get_session_id = "select id from sessions where date='{}' and userid='{}'"