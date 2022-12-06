import os
import mcstasscript as ms

def make_instrument():
    instrument = ms.McStas_instr("mystery_3", input_path="run_folder")
    instrument.settings(output_path=os.path.join("data_folder", "instrument_3"))

    instrument.add_parameter("double", "wavelength", value=6.0, comment="[AA]  Mean wavelength of neutrons")
    instrument.add_parameter("double", "d_wavelength", value=0.05, comment="[AA]  Wavelength spread of neutrons")
    instrument.add_parameter("double", "r", value=150.0, comment="[AA]  Radius of scattering hard spheres")
    instrument.add_parameter("double", "PHI", value=0.001, comment="[1]  Particle volume fraction")
    instrument.add_parameter("double", "Delta_Rho", value=6E10, comment="[cm^-2]  Scattering length density")
    instrument.add_parameter("double", "frac_dir", value=0.03, comment="[1]  Fraction of statistics for direct beam")
    instrument.add_parameter("double", "frac_inc", value=0.01, comment="[1]  Fraction of statistics for incoherent scattering in scattered beam")
    instrument.add_declare_var("int", "was_scattered")


    source = instrument.add_component("source", "Source_simple")
    source.radius = 0.02
    source.dist = 6
    source.focus_xw = 0.01
    source.focus_yh = 0.01
    source.lambda0 = "wavelength"
    source.dlambda = "d_wavelength"
    source.flux = 1e8

    coll1 = instrument.add_component("coll1", "Slit")
    coll1.radius = 0.005
    coll1.set_AT(['0', ' 0', ' 3'], RELATIVE=source)

    coll2 = instrument.add_component("coll2", "Slit")
    coll2.radius = 0.005
    coll2.set_AT(['0', ' 0', ' 6'], RELATIVE=source)

    sample_position = instrument.add_component("sample_position", "Arm")
    sample_position.set_AT(['0', '0', '0.2'], RELATIVE="coll2")

    sample_conventional = instrument.add_component("sample_conventional", "SANS_spheres2")
    sample_conventional.set_SPLIT(100)
    sample_conventional.xwidth = 0.02
    sample_conventional.yheight = 0.02
    sample_conventional.zthick = 0.001
    sample_conventional.sc_aim = "(1-frac_dir)"
    sample_conventional.sans_aim = "(1-frac_inc)"
    sample_conventional.R = "r"
    sample_conventional.append_EXTEND("was_scattered=SCATTERED;")
    sample_conventional.set_SPLIT("")
    sample_conventional.set_AT(['0', '0', '0'], RELATIVE="sample_position")

    PSDrad = instrument.add_component("PSDrad", "PSD_monitor_rad")
    PSDrad.filename = "\"psd2.dat\""
    PSDrad.filename_av = "\"psd2_av.dat\""
    PSDrad.rmax = 0.3
    PSDrad.set_WHEN("was_scattered")
    PSDrad.set_AT(['0', ' 0', ' 3.02'], RELATIVE="sample_position")

    PSDrad_full = instrument.add_component("PSDrad_full", "PSD_monitor_rad")
    PSDrad_full.filename = "\"psd2_full.dat\""
    PSDrad_full.filename_av = "\"psd2_av_full.dat\""
    PSDrad_full.rmax = 0.3
    PSDrad_full.set_AT(['0', ' 0', ' 3.02'], RELATIVE="sample_position")

    return instrument
