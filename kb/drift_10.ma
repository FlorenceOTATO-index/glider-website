behavior_name=drift_at_depth
# drift_10.ma
# 2016/9/1  	dkaragon    initial for ud_134 100 m glider
# 2020/12/8 	dkaragon	modified for L3 shallow hover 2-3 m; uncomment thruster section for ru33!
# 2022/10/25	dkaragon	modified for passengers with thruster
# 2022/11/8		dkaragon	some changes after test dive.  it was thrusting down pitch OK but was adjusting the pump eventhough it was in deadband, not really sure why, increased the time to adjust pump

<start:b_arg>
    b_arg: end_action(enum)             2       # 2-resume
	
	# Should be ignored if start_when not UTC
	b_arg: when_utc_timestamp(dtime)	-1
	b_arg: when_secs(sec)				180		# in surface beh 0 means UTC just once
	
    b_arg: stop_when_hover_for(sec)     28800.0	# terminate hover when depth does not change for
    b_arg: est_time_to_settle(s)        180.0	# Not sure, how long it should take to get to hover pos?
    b_arg: target_depth(m)              315		# depth to drift at
    b_arg: target_altitude(m)           -1      # altitude to drift at, <=0 disables
    b_arg: alt_time(s)                  -1      # time spacing for altimeter pings
    
    ### Shallow pump values
    b_arg: target_deadband(m)           40		# +/- around target depth
    b_arg: start_dist_from_target(m)    10    	# Start drift x m away: -1 means use the target_deadband
    b_arg: depth_ctrl(enum)             2       # 0 = Buoyancy pump, 2 = pitch
    b_arg: bpump_delta_value(cc)        50.0	# Increments to adjust x_hover_ballast(cc) for nuetral
    b_arg: bpump_deadz_width(cc)        30.0    # For temporarily adjusting the buoyancy pump
    b_arg: bpump_db_frac_dz(nodim)      0.66    # deadband during the drift_at_depth behavior
    b_arg: bpump_delay(s)               240      # mininum time between adjustments

    # Pitch/steering Parameters
    b_arg: use_pitch(enum)              3       # 3  Servo on Pitch
    b_arg: pitch_value(X)               0.0     # radians or in
    b_arg: wait_for_pitch(bool)         1       # wait to adjust ballast when pitch in deadband
    b_arg: enable_steering(bool)        1
	
	# Thruster
	b_arg: use_thruster(enum)   		4		# 0  Not in use, 1 % glider V, 2 % max thruster V, 4 Watts
    b_arg: thruster_value(X)   			7		# based on above

    # Dive to hover zone
    b_arg: d_use_bpump(enum)            2		# 2 absolute
    b_arg: d_bpump_value(X)             -1000.0
    b_arg: d_use_pitch(enum)            3       # servo on pitch
    b_arg: d_pitch_value(X)             -0.45 	# dive a little slower?
    # Climb to hover zone (likely brought to surface by surfacing behavior, not hover)
    b_arg: c_use_bpump(enum)            2
    b_arg: c_bpump_value(X)             260.0
    b_arg: c_use_pitch(enum)            3       # servo on pitch
    b_arg: c_pitch_value(X)             0.3		# 20 degrees

    b_arg: battpos_db(nodim)            .5		# .2 is TWR default, might be too twitchy, try .5 first   
	
	# Thruster Settings
	# b_arg: use_thruster(enum)   		0  		# 0  Not in use								
    # b_arg: thruster_value(X)			0    	# use_thruster == 0  None
	
	# Arguments for pitch depth controller (depth_ctrl = 2 )
    b_arg: depth_pitch_limit(rad) 		0.174	# limit pitch response to 10 deg
	b_arg: depth_pitch_max_time(s) 		240		# Max time at maximum u_hover_depth_pitch_limit before we start to adjust ballast

<end:b_arg>

