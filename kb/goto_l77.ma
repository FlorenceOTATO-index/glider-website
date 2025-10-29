behavior_name=goto_list
# goto_l77.ma, for electa (1000M/200M HD pump)

<start:b_arg>
	b_arg: num_legs_to_run(nodim) -2  # -1   loop forever, -2 traverse once
	b_arg: start_when(enum) 0 # BAW_IMMEDIATELY
	b_arg: list_stop_when(enum) 7 # BAW_WHEN_WPT_DIST
	b_arg: list_when_wpt_dist(m) 1000
	b_arg: initial_wpt(enum) -1 # 0 is first, 1 is second, -1 is first since last wpt hit
	b_arg: num_waypoints(nodim)  2
<end:b_arg>

<start:waypoints>
# LONGITUDE LATITUDE
#-7348.000  3917.000
#-7329.000  3818.000
-7338.000  3808.000
-7427.000  3812.000
<end:waypoints>
