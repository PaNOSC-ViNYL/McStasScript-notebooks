import os
import mcstasscript as ms

def make_instrument():
    instrument = ms.McStas_instr("mystery_2", input_path="run_folder")
    instrument.settings(output_path=os.path.join("data_folder", "instrument_2"))

    instrument.add_parameter("double", "Lmin", value=0.5, comment="[AA] Lower edge of wavelength band")
    instrument.add_parameter("double", "Wavelength_band", value=1.8, comment="[AA] Width of wavelength band")
    instrument.add_parameter("double", "npulses", value=1.0,
                             comment="[1] Number of pulses from source",
                             options=[1, 2, 3, 4, 5, 6])

    instrument.add_declare_var("int", "npulses_declare")
    instrument.add_declare_var("double", "Lmax")
    instrument.add_declare_var("double", "Lcenter")

    instrument.append_initialize("npulses_declare=npulses; ")
    instrument.append_initialize("Lmax = Lmin + Wavelength_band; ")

    instrument.add_declare_var("double", "sample_position", value=160)

    Source = instrument.add_component("Source", "Source_simple")
    Source.yheight = 0.03
    Source.xwidth = 0.03
    Source.dist = 2.0
    Source.focus_xw = 0.03
    Source.focus_yh = 0.03
    Source.lambda0 = "Lmin + 0.5*Wavelength_band"
    Source.dlambda = "0.5*Wavelength_band"
    Source.flux = 1E13
    Source.append_EXTEND("double t_between_pulses=1.0/14.0;")
    Source.append_EXTEND("double pulse_n=(double) floor(rand01()*npulses_declare);")
    Source.append_EXTEND("double pulse_delay=t_between_pulses*pulse_n;")
    Source.append_EXTEND("t=2860*rand01()*1E-6 + pulse_delay;")

    instrument.add_declare_var("double", "tmax_source")
    instrument.append_initialize("tmax_source = 3000 + 1.1*1E6*(npulses-1)*1/14.0;")
    
    guide1 = instrument.add_component("guide1", "Guide_gravity")
    guide1.set_parameters(w1=Source.focus_xw, h1=Source.focus_yh,
                          m=4, G=-9.82,
                          l="chopper_position - " + str(Source.dist) + "- 0.02")
    guide1.set_AT(Source.dist, RELATIVE=Source)

    instrument.add_parameter("double", "enable_chopper_1", value=1,
                             comment="Enable clockwise chopper", options=[0, 1])
    instrument.add_parameter("double", "enable_chopper_2", value=1,
                             comment="Enable counter clockwise chopper", options=[0, 1])

    instrument.add_declare_var("double", "speed")
    instrument.add_declare_var("double", "delay")
    instrument.add_declare_var("double", "chopper_position", value=6.5)
    instrument.append_initialize("Lcenter = Lmin + 0.5*Wavelength_band; ")
    instrument.append_initialize("speed = 2.0*PI/Lcenter*K2V; ")
    instrument.append_initialize("delay = chopper_position/speed; ")
    instrument.append_initialize("delay = delay + 1.340E-3; ")
    instrument.add_parameter("frequency_multiplier", value=1,
                             comment="[1] Chopper frequency as multiple of source frequency")

    chopper = instrument.add_component("chopper", "DiskChopper")
    chopper.theta_0 = 4.0
    chopper.radius = 0.35
    chopper.yheight = 0.03
    chopper.nu = "frequency_multiplier*14.0"
    chopper.delay = "delay"
    chopper.nslit = 1
    chopper.set_AT([0, 0, 'chopper_position - 0.005'], RELATIVE=Source)
    chopper.set_WHEN("enable_chopper_1 > 0.5")

    counter_chopper = instrument.add_component("counter_chopper", "DiskChopper")
    counter_chopper.theta_0 = 4.0
    counter_chopper.radius = 0.35
    counter_chopper.yheight = 0.03
    counter_chopper.nu = "-frequency_multiplier*14.0"
    counter_chopper.delay = "delay"
    counter_chopper.nslit = 1
    counter_chopper.set_AT([0, 0, 'chopper_position + 0.005'], RELATIVE=Source)
    counter_chopper.set_WHEN("enable_chopper_2 > 0.5")
    
    """
    guide2 = instrument.add_component("guide2", "Guide_gravity")
    guide2.set_parameters(w1=Source.focus_xw, h1=Source.focus_yh,
                         m=3, G=-9.82,
                         l="sample_position - chopper_position - 0.5")
    guide2.set_AT(0.015, RELATIVE=counter_chopper)
    """
    
    guide2 = instrument.add_component("guide2", "Elliptic_guide_gravity")
    guide2.set_parameters(xwidth=Source.focus_xw, yheight=Source.focus_yh,
                         m=3, dimensionsAt='"entrance"',
                         l="sample_position - chopper_position - 0.5",
                         loutxw=0.55, loutyh=0.55, linxw=2.0, linyh=2.0)
    guide2.set_AT(0.015, RELATIVE=counter_chopper)

    instrument.add_declare_var("double", "speed_max")
    instrument.append_initialize("speed_max = 2*PI/Lmin*K2V;")

    instrument.add_declare_var("double", "speed_min")
    instrument.append_initialize("speed_min = 2*PI/Lmax*K2V;")

    instrument.add_declare_var("double", "sample_tmin")
    instrument.add_declare_var("double", "sample_tmax")
    instrument.append_initialize("sample_tmin = 0.9*1E6*sample_position/speed_max;")
    instrument.append_initialize("sample_tmax = 1.1*1E6*sample_position/speed_min + tmax_source;")

    Sample = instrument.add_component("Sample", "Powder1", SPLIT=200)
    Sample.radius = 0.003
    Sample.yheight = 0.02
    Sample.q = 5
    Sample.d_phi = 12
    Sample.set_AT([0, 0, 'sample_position'], RELATIVE=Source)
    Sample.append_EXTEND("if (!SCATTERED) ABSORB;")

    TOF_cylPSD = instrument.add_component("TOF_cylPSD", "TOF_cylPSD_monitor")
    TOF_cylPSD.nt = 200
    TOF_cylPSD.nphi = 180
    TOF_cylPSD.filename = '"TOF_cylPSD"'
    TOF_cylPSD.radius = 2.0
    TOF_cylPSD.yheight = 0.20
    TOF_cylPSD.tmin = "sample_tmin"
    TOF_cylPSD.tmax = "sample_tmax"
    TOF_cylPSD.restore_neutron = 1
    TOF_cylPSD.set_AT([0, 0, 0], RELATIVE=Sample)

    instrument.add_parameter("double", "two_theta", value=90.0, comment="[deg] TOF det 2 theta")

    TOFdetArm = instrument.add_component("TOFdetArm", "Arm")
    TOFdetArm.set_AT([0, 0, 0], RELATIVE=Sample)
    TOFdetArm.set_ROTATED([0, 'two_theta', 0], RELATIVE=Sample)

    TOFdet = instrument.add_component("TOFdet", "TOF_monitor")
    TOFdet.nt = 100
    TOFdet.filename = '"TOFdet"'
    TOFdet.xwidth = 0.01
    TOFdet.yheight = 0.2
    TOFdet.tmin = 70000
    TOFdet.tmax = 80000
    TOFdet.restore_neutron = 1
    TOFdet.set_AT([0, 0, 2.001], RELATIVE=TOFdetArm)
    
    return instrument
