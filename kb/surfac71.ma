behavior_name=surface
# climb to surface with ballast pump full out
# pitch servo'ed to 26 degrees
# Hand Written
# 10 July 2010 ballsup@webbresearch.com based on legacy surfac10.ma
# 2016-02-27 gong@vims.edu
# 2016-02-28 gong@vims.edu tuning the surfacing interval so that only two full dives are completed when diving to 350m (8400 seconds).
# 2016-02-29 gong@vims.edu changing back to 2 hours, still tuning for two dives to 350m
# 2016-03-13 gong@vims.edu changing to 1 hour internval on the morning of recovery
# 2018-04-30 gong@vims.edu validated for amelia on MARACOOS run testing for NPP

# Come up if haven't had comms for a while, X minutes

<start:b_arg>

#    b_arg: start_when(enum)         12            # BAW_NOCOMM_SECS 12, when have not had comms for WHEN_SECS secs
    b_arg: end_action(enum)         1             # 0-quit, 1 wait for ^C quit/resume, 2 resume, 3 drift til "end_wpt_dist"

    b_arg: when_secs(sec)           7200          # Surface every x seconds for no comms

    b_arg: gps_wait_time(s)         600           # how long to wait for gps
    b_arg: keystroke_wait_time(sec) 420           # how long to wait for control-C
    b_arg: when_wpt_dist(m)         300            # how close to waypoint before surface, only if start_when==7

    b_arg: c_use_bpump(enum)        2           # use buoyancy absolute on surfacing climb, 0 is autoballast
    b_arg: c_bpump_value(x)         50
    b_arg: c_use_pitch(enum)        3             # 3:servo (command by angle), 1: battpos (command by battery position)
    b_arg: c_pitch_value(X)         0.4538        # if use_pitch is 1, then unit in inch; if use_pitch is 3, unit is in radian, 0.4 rad = 20 deg

    b_arg: c_use_thruster(enum)   0               # 3  Command depth rate.  See sensors for use_thruster = depthrate
    b_arg: c_thruster_value(X)   -0.05           # use_thruster == 3  m/s, desired depth rate. < 0 for climb
    b_arg: c_stop_when_air_pump(bool)  1        # Terminate climb once air pump has been inflated. For use with thruster only.

    b_arg: printout_cycle_time(sec) 60.0 # How often to print dialog

<end:b_arg>
