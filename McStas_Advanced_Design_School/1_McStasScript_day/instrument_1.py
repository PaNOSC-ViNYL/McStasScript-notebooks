import os
import mcstasscript as ms

def make_instrument():
    instrument = ms.McStas_instr("mystery_1", input_path="run_folder")
    instrument.settings(output_path=os.path.join("data_folder", "instrument_1"))

    instrument.add_user_var("double", "flag1")
    instrument.add_user_var("double", "flag2")

    src = instrument.add_component("Source", "Source_simple")
    src.set_parameters(xwidth=0.1, yheight=0.1, focus_xw=0.04, focus_yh=0.06, dist=2)
    energy_i = instrument.add_parameter("energy_i", value=10.0, comment="Initial energy in [meV]")
    energy_f = instrument.add_parameter("energy_f", value=8.0, comment="Final energy in [meV]")
    src.E0 = energy_i
    src.dE = "0.01*energy_i"

    guide1 = instrument.add_component("guide1", "Guide_gravity")
    guide1.set_parameters(w1=src.focus_xw, h1=src.focus_yh,
                         m=2, G=-9.82, l=15)
    guide1.set_AT(src.dist, RELATIVE=src)

    guide2 = instrument.add_component("guide2", "Guide_gravity")
    guide2.set_parameters(w1=guide1.w1, h1=guide1.h1,
                         w2=guide1.w1*0.9, h2=guide1.h1*0.9,
                         m=2, G=-9.82, l=10)
    guide2.set_AT(guide1.l + 0.01, RELATIVE=guide1)
    guide2.set_ROTATED([0, 0.7, 0], RELATIVE=guide1)

    mono_Q = instrument.add_declare_var("double", "mono_Q", value=1.714) # Q for Ge 311
    anna_Q = instrument.add_declare_var("double", "anna_Q", value=1.677) # Q for PG 004
    
    instrument.add_declare_var("double", "wavevector_i")
    instrument.add_declare_var("double", "wavevector_f")
    instrument.append_initialize("wavevector_i = sqrt(energy_i)*SE2V*V2K;")
    instrument.append_initialize("wavevector_f = sqrt(energy_f)*SE2V*V2K;")

    mono_rotation = instrument.add_declare_var("double", "mono_rotation")
    anna_rotation = instrument.add_declare_var("double", "anna_rotation")
    instrument.append_initialize("mono_rotation = asin(mono_Q/(2.0*wavevector_i))*RAD2DEG;")
    instrument.append_initialize("anna_rotation = asin(anna_Q/(2.0*wavevector_f))*RAD2DEG;")

    mono = instrument.add_component("mono", "Monochromator_flat")
    mono.zwidth = 0.05
    mono.yheight = 0.08
    mono.Q = mono_Q
    mono.set_AT(guide2.l + 0.5, RELATIVE=guide2)
    mono.set_ROTATED([0, mono_rotation, 0], RELATIVE=guide2)

    beam_direction = instrument.add_component("beam_dir_mono", "Arm", AT_RELATIVE=mono)
    beam_direction.set_ROTATED([0, mono_rotation, 0], RELATIVE=mono)

    slit = instrument.add_component("slit_m_s", "Slit")
    slit.radius = 0.03
    slit.set_AT(0.6, RELATIVE=beam_direction)

    sample_position = instrument.add_component("sample_pos", "Arm")
    sample_position.set_AT(0.2, RELATIVE=slit)

    A3 = instrument.add_parameter("A3", value=-43.3, comment="Sample rotation in [deg]")
    sample = instrument.add_component("sample", "Phonon_simple", RELATIVE=sample_position)
    sample.set_ROTATED([0, A3, 0])
    sample.set_parameters(radius=0.015, yheight=0.05, target_index=2, focus_r=0.03,
                          sigma_abs=0.17, sigma_inc=0.003, b=0.90, M=208,
                          c=8, a=4.95, DW=1.00, T=300)
    
    A4 = instrument.add_parameter("A4", value=72.69, comment="Analyzer position in [deg]")
    beam_direction = instrument.add_component("beam_dir_sample", "Arm", AT_RELATIVE=sample)
    beam_direction.set_ROTATED([0, A4, 0], RELATIVE=sample_position)
    
    slit = instrument.add_component("slit_s_a", "Slit")
    slit.radius = 0.03
    slit.set_AT(0.3, RELATIVE=beam_direction)
    
    anna = instrument.add_component("anna", "Monochromator_flat")
    anna.zwidth = 0.05
    anna.yheight = 0.08
    anna.Q = anna_Q
    anna.set_AT(0.5, RELATIVE=beam_direction)
    anna.set_ROTATED([0, anna_rotation, 0], RELATIVE=beam_direction)
    
    beam_direction = instrument.add_component("beam_dir_anna", "Arm", AT_RELATIVE=anna)
    beam_direction.set_ROTATED([0, anna_rotation, 0], RELATIVE=anna)
    
    slit = instrument.add_component("slit_a_d", "Slit")
    slit.xwidth = 0.05
    slit.yheight = 0.08
    slit.set_AT(0.4, RELATIVE=beam_direction)
    
    PSD = instrument.add_component("PSD", "PSD_monitor")
    PSD.set_AT(0.5, RELATIVE=beam_direction)
    PSD.set_parameters(nx=50, ny=50, xwidth=0.05, yheight=0.08,
                       filename='"PSD.dat"', restore_neutron=1)

    return instrument
