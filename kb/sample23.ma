behavior_name=sample
# sample all science sensors on dive/hover/climb
# 2013-Apr-24 lacooney@alum.mit.edu Modified from sample10.ma
# 2021-Aug-25 gong@vims.edu adopted for electa G3S glider

<start:b_arg>
   b_arg: sensor_type(enum)                48 #! choices = sensor_type()
                                              # ALL	 0  C_SCIENCE_ALL_ON
                                              # PROFILE     1  C_PROFILE_ON
                                              # FLBBCD     48  C_FLBBCD_ON
                                              # DMON       49  C_DMON_ON
                                              # SUNA       51  C_SUNA_ON
                                              # SATPAR     52  C_SATPAR_ON
                                              # OXY4       54  C_OXY4_ON
                                              # BSIPAR     56  C_BSIPAR_ON
                                              # echosndr853 60 C_ECHOSNDR853_ON
                                              # <PROTO> pick next number here for new proglet
                                              #  REQUIRED: also add it to: science_super.c: __ss_indexes[],
                                              #  add it to output_sensors[] in snsr_in.c,
                                              #  and update header doco in sample.c.

                                                # This is a bit-field, combine:
                                                # 8 on_surface, 4 climbing, 2 hovering, 1 diving
    b_arg: state_to_sample(enum)            15  # 0  none
                                                # 1  diving
                                                # 2  hovering
                                                # 4  climbing
                                                # 8  on_surface
                                                # 15 diving|hovering|climbing|on_surface

	b_arg: sample_time_after_state_change(s)  15  #! simple = False; min = 0.0
                                                 # time after a positional stat
                                                 # change to continue sampling


    b_arg: intersample_time(s)                0  # if < 0 then off, if = 0 then
                                                 # as fast as possible, and if
                                                 # > 0 then that many seconds
                                                 # between measurements

    b_arg: nth_yo_to_sample(nodim)            1  # After the first yo, sample only
                                                 # on every nth yo. If argument is
                                                 # negative then exclude first yo.

    b_arg: intersample_depth(m)              -1  # supersedes intersample_time
                                                 # by dynamically estimating
                                                 # and setting intersample_time
                                                 # to sample at the specified
                                                 # depth interval. If <=0 then
                                                 # then sample uses
                                                 # intersample_time, if > 0 then
                                                 # that many meters between
                                                 # measurements

    b_arg: min_depth(m)                      -5  # minimum depth to collect data, default
                                                 # is negative to leave on at surface in
                                                 # spite of noise in depth reading
    b_arg: max_depth(m)                    2000  # maximum depth to collect data

<end:b_arg>
