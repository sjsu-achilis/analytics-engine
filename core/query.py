# -*- coding: utf-8 -*-
get_hydration = "select event_timestamp, metric_value from \
health_metrics where userid='{}' and metric_label='hydration' \
and event_timestamp::date between '{}' and '{}'"
