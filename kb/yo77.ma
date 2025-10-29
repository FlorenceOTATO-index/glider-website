behavior_name=yo
# 2013-Nov-01 gong@vims.edu The goal is to fly slow and use as little power as possible.
# 2016-Feb-26 gong@vims.edu set for standard flight for MARACOOS 2016 Wilmington Canyon deployment
# 2016-Mar-08 gong@vims.edu modified for transit back to pick up location offshore of DE. thruster will be on for dive and climb at 2 watt.
# 2021-Aug-25 gong@vims.edu modified for electa's first deployment of MD coast
# 2022-Apr-12 gong@vims.edu modified for electa's deployment of NJ coast
# 2023-Nov-11 lnferris@vims.edu modified for Norwegian sea (full bpump, default 26 deg to start)

<start:b_arg>
    b_arg: start_when(enum)      2    # set in mission file
    b_arg: num_half_cycles_to_do(nodim)  -1  # default is -1, surfacing NOT based on number of half yo's

    # dive

    b_arg: d_target_depth(m)      200  # 345 normally
    b_arg: d_target_altitude(m)   6  # default is 8, -1 to turn off

    b_arg: d_use_bpump(enum)      2    # 0 for auto, 2 for buoyancy absolute
    b_arg: d_bpump_value(x)      -425  # positive number for autoballast (330 worked well for normal flight, 400 for speed burst?)

    b_arg: d_use_pitch(enum)      3  # servo, set dive angle
    b_arg: d_pitch_value(X)       -0.4   # 0.36 for 20 deg, 0.4528 for 26 deg, 0.523 for 30 deg, 0.611 for 35 deg
    #b_arg: d_use_pitch(enum)      1  # battpos
    #b_arg: d_pitch_value(X)       -0.04   # inches for d_bpump_value of -420, -23 deg

    b_arg: d_use_thruster(enum)   0
    b_arg: d_thruster_value(X)    3

    # climb
    b_arg: c_target_depth(m)      5
    b_arg: c_target_altitude(m)  -1

    b_arg: c_use_bpump(enum)      2  # buoyancy absolute
    b_arg: c_bpump_value(x)       -100  # cc

    b_arg: c_use_pitch(enum)      3         #  servo for angle
    b_arg: c_pitch_value(X)       0.4    # rad, 0.36 for 20 deg, 0.4528 for 26 deg, 0.523 for 30 deg, 0.611 for 35 deg
    #b_arg: c_use_pitch(enum)      1         #  battpos
    #b_arg: c_pitch_value(X)       0    #  inches for c_bpump_value of 225, 20 deg

    b_arg: c_use_thruster(enum)   0
    b_arg: c_thruster_value(X)    4         #  -0.10 m/s for c_use_thruster = 3

    b_arg: end_action(enum) 2     # 0-quit, 2 resume, set in mission file
<end:b_arg>
