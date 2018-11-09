# -*- coding: utf-8 -*-
get_metric = "select event_timestamp, metric_value from \
health_metrics where userid='{}' and metric_label='{}' \
and event_timestamp::date between '{}' and '{}'"

get_max_metric = "select event_timestamp, max(metric_value) from \
health_metrics where userid='{}' and metric_label='{}' \
and event_timestamp::date between '{}' and '{}' group by event_timestamp"

get_questions = "select * from questionnaire"

save_response_ins = "insert into questionnaire_response values {}"

edit_qstn_response = "update questionnaire_response set response={} where userid='{}' and qid='{}'"

get_sports = "select * from sports"

is_uid_available = "select userid from users"

register_user_info_1 = "insert into users values {}"

register_user_info_2 = "insert into user_information values {}"