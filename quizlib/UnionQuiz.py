import mcstasscript as ms

from .quiz import Quiz, make_red, make_green, make_orange
from .helpers import name_of_component_type

class UnionQuiz(Quiz):
    def __init__(self):
        super().__init__()


    def question_1(self, answer=None):
        """
        What is not a reasons to use Union components:
        A: Want to describe complex geometry
        B: Combination of physical processes in one geometry
        C: Multiple scattering between geometries / processes
        D: Model detector systems
        E: Logging of scattering
        F: Logging of absorption
        G: Gravity support
        H: Tracking of features in data
        """

        feedback = {"A": "The Union components can be used to simulate highly complex geometries!",
                    "B": "Union materials can contain an unlimited number of scattering processes.",
                    "C": "All multiple scattering will be handled, even between geometries.",
                    "D": "With the absorption loggers the absorption in detectors can be modelled.",
                    "E": "The Union components have powerful logger components that log scattering.",
                    "F": "The Union components have powerful abs_logger components that log absorption.",
                    "G": "The Union components ignores gravity, so the Union components may not be the right option if gravity effects are important in the described area.",
                    "H": "The Union components have several features for tracking interesting features in data.",
                    }

        self.multiple_choice(answer=answer, correct_answer="G", feedback=feedback)

    def question_2(self, answer=None):
        """
        Important limitation to remember when using Union components

        No perfectly overlapping edges
        Maximum 10 geometries
        Maximum 5 processes in a material
        One Union system per instrument
        """

        feedback = {"A": "Two geometries should overlap or be separate, not share a face.",
                    "B": "There are no limits to the number of geometries simulated.",
                    "C": "There are no limits to the number of processes in a material.",
                    "D": "It is allowed to have several distinct Union systems in an instrument."
                    }

        self.multiple_choice(answer=answer, correct_answer="A", feedback=feedback)

    def question_3(self, answer=None):
        """
        What does a process component do?

        Describes a number of scattering mechanisms
        Describes a physical process
        Describes absorption
        """

        feedback = {"A": "A process component describes just one kind of scattering.",
                    "B": "Yes! It describes a single scattering mechanism.",
                    "C": "No, absorption is handled elsewhere.",
                    }

        self.multiple_choice(answer=answer, correct_answer="B", feedback=feedback)

    def question_4(self, answer=None):
        """
        What is meant by a material in Union? (created by Union_make_material)

        Connects any single process to a absorption description
        Collects a number of processes and absorption description
        Materials are not user defined
        The position and rotation of material components are important
        """

        feedback = {"A": "No, each process does not get individual absorption, its handled differently.",
                    "B": "Yes, a material collects an arbitrary number of processes and one description of absorption.",
                    "C": "The Union_make_material component is used to create user defined materials.",
                    "D": "No, they are completely ignored as a material has no placement in space."
                    }

        self.multiple_choice(answer=answer, correct_answer="B", feedback=feedback)

    def question_5(self, answer=None):
        """
        Which statement about geometry components below is true?

        Geometry components can take multiple material definitions
        Geometry components are optional for running a Union simulation
        The position and rotation of geometry components are important
        The geometry component performs the simulation
        """

        feedback = {"A": "No, a geometry component take at most a single material definition.",
                    "B": "No, without geometry components there will be nothing simulated.",
                    "C": "Yes, the geometry component describes something physical which is placed in space.",
                    "D": "No, the geometry components themselves do not contain any simulation code."
                    }

        self.multiple_choice(answer=answer, correct_answer="C", feedback=feedback)

    def question_6(self, answer=None):
        """
        What is the responsibility of a logger component?

        A logger records absorbed intensity
        A logger records scattering intensity
        A logger records the final state of the ray
        A logger always records positions
        """

        feedback = {"A": "No, that would be an abs_logger component!",
                    "B": "Yes, it records scattered intensity along some axis defined by the individual logger component.",
                    "C": "No, the important aspect of loggers is that they can access scattering step of the simulation.",
                    "D": "No, the scattered intensity could be recorded as function of something different, for example energy or momentum transfer."
                    }

        self.multiple_choice(answer=answer, correct_answer="B", feedback=feedback)

    def question_7(self, answer=None):
        """
        What is the responsibility of an abs_logger component?

        An abs_logger records the final weight of each ray
        An abs_logger needs to be connected to a specific geometry
        An abs_logger records scattering intensity
        An abs_logger records absorbed intensity
        """

        feedback = {"A": "No, the abs_loggers records absorption along the entire path of the ray.",
                    "B": "No, it doesn't need to, but it can be if only absorption in that geometry is desired.",
                    "C": "No, the regular logger components perform that role.",
                    "D": "Yes, it records absorbed intensity along the path of the ray.",
                    }

        self.multiple_choice(answer=answer, correct_answer="D", feedback=feedback)

    def question_8(self, answer=None):
        """
        What is the purpose of a conditional component?

        A conditional component decides when a geometry is simulated
        A conditional component can affect exactly one other component
        A conditional component imposes a condition on logger or abs_logger components
        A conditional component is required to perform a simulation with Union components
        """

        feedback = {"A": "No, that is done using the number_of_activation parameter on a geometry.",
                    "B": "No, a conditional component can affect multiple loggers / abs_loggers.",
                    "C": "Yes, it defines a condition on the final ray and imposes that on loggers / abs_loggers.",
                    "D": "No, conditional components are a specialized tool not frequently used."
                    }

        self.multiple_choice(answer=answer, correct_answer="C", feedback=feedback)

    def question_9(self, answer=None):
        """
        Select the true statement about the Union_master component.

        There can only be one master component in an instrument
        A Union_master component is required to perform a simulation with Union components
        All Union components in an instrument file are simulated in a master component
        The Union_master needs to be placed on a Union geometry
        """

        feedback = {"A": "No, there is no limitation on the number of master components in an instrument.",
                    "B": "Yes, without a master the rays in McStas are not affected by anything Union.",
                    "C": "No, a master component only simulates geometries defined earlier than itself.",
                    "D": "No, the location of the Union_master component doesn't really matter, all the location data is stored in the geometries."
                    }

        self.multiple_choice(answer=answer, correct_answer="B", feedback=feedback)

    def question_10(self, answer=None):
        """
        The geometry with highest priority decides what material to be simulated
        The geometry with lowest priority decides what material to be simulated
        The priority of a geometry decides how likely it is a ray scatters from it
        """

        feedback = {"A": "Yes, when multiple geometries cover a point, the one with highest priority decides the material.",
                    "B": "No, the Union components defines a higher priority to be more important.",
                    "C": "No, there is a parameter called p_interact on geometries for that purpose.",
                    }

        self.multiple_choice(answer=answer, correct_answer="A", feedback=feedback)

    def question_11(self, answer=None):
        required_pars = {"sigma": 4*0.0082, "unit_cell_volume": 66.4}

        msg = "The incoherent process component was found with the right parameters"

        required_component = "Incoherent_process"
        comp_name = name_of_component_type(answer, required_component=required_component)
        if comp_name is None:
            return

        self.last_component_in_instr_check(answer, comp_type_str=required_component,
                                           required_pars=required_pars, success_msg=msg)

    def question_12(self, answer=None):
        required_pars = {"reflections": '"Al.laz"'}

        msg = "The powder process component was found with the right parameters"

        required_component = "Powder_process"
        comp_name = name_of_component_type(answer, required_component=required_component)
        if comp_name is None:
            return

        self.last_component_in_instr_check(answer, comp_type_str=required_component,
                                           required_pars=required_pars, success_msg=msg)

    def question_13(self, answer=None):

        inc_name = name_of_component_type(answer, required_component="Incoherent_process")
        if inc_name is None:
            return

        pow_name = name_of_component_type(answer, required_component="Powder_process")
        if pow_name is None:
            return

        # Could improve code to understand each permutation
        expected_process_string = f'"{inc_name},{pow_name}"'

        required_pars = {"my_absorption": 100*4*0.231/66.4, "process_string": expected_process_string}

        msg = "The material component was found with the right parameters"

        required_component = "Union_make_material"
        comp_name = name_of_component_type(answer, required_component=required_component)
        if comp_name is None:
            return

        self.last_component_in_instr_check(answer, comp_type_str=required_component,
                                           required_pars=required_pars, success_msg=msg)

    def question_14(self, answer=None):
        # Check there are two single_crystal_process components

        if answer is None:
            print("Insert your answer in the question above.")
            return None

        if not isinstance(answer, ms.interface.instr.McStas_instr):
            print(make_red("Have to provide an instrument object as answer"))
            return

        #type_name_dict = {x.component_name: x.name for x in answer.component_list}
        types = [x.component_name for x in answer.component_list]
        xtal_process_count = types.count("Single_crystal_process")

        if xtal_process_count == 1:
            print(make_red("Only see one Single_crystal_process in the provided instrument"))
            return

        if xtal_process_count > 2:
            print(make_red("See more than two single crystal processes in the instrument!"))
            return

        # Finds last single crystal, the one that should be modified
        single_crystal = name_of_component_type(answer, required_component="Single_crystal_process")
        if single_crystal is None:
            return

        required_pars = {"reflections": '"YBaCuO.lau"', "mosaic":15, "packing_factor":0.5, "ax":3.8186, "by":3.886, "cz":11.6777}
        required_component = "Single_crystal_process"
        msg = "Twinned single crystal process found with correct parameters!"
        self.last_component_in_instr_check(answer, comp_name=single_crystal, comp_type_str=required_component,
                                           required_pars=required_pars, success_msg=msg,
                                           required_ROTATED_relative="ABSOLUTE",
                                           required_ROTATED_data=["twin_x", "twin_y", "twin_z"])


        required_component = "Union_make_material"
        comp_name = name_of_component_type(answer, required_component=required_component)
        if comp_name is None:
            return

        # Could improve code to understand each permutation
        #expected_process_string = f'"{inc_name},{pow_name}"'

        required_pars = {"my_absorption": 100*14.82/173.28}#, "process_string": expected_process_string}

        msg = "The material component was found with the right parameters!"

        self.last_component_in_instr_check(answer, comp_type_str=required_component,
                                           required_pars=required_pars, success_msg=msg)

    def question_15(self, answer=None):
        pass

    def question_16(self, answer=None):
        pass

    def question_17(self, answer=None):
        pass

    def question_18(self, answer=None):
        pass

    def question_19(self, answer=None):
        pass

    def question_20(self, answer=None):
        """
        Which twin axis impact the L_monitor the least?

        twin_x
        twin_y
        twin_z
        """

        feedback = {
            "A": "No, it is assumed they all are quite close to 0, try around there.",
            "B": "No, it is assumed they all are quite close to 0, try around there.",
            "C": "Exactly, it doesn't impact it at all (when the others are 0).",
            }

        self.multiple_choice(answer=answer, correct_answer="C", feedback=feedback)

    def question_21(self, answer=None):
        pass



    def question_old(self, answer=None):
        """
        Question: Will there be multiple scattering between sphere 1 and 2?
        A: 1 -> 2
        B: 2 -> 1
        C: Yes
        D: No
        """

        feedback = {"A": "The Union simulation engine will ensure multiple scattering both ways.",
                    "B": "The Union simulation engine will ensure multiple scattering both ways.",
                    "C": "All multiple scattering will be handled!",
                    "D": "The master will handle multiple scattering between the geometries."
                    }

        self.multiple_choice(answer=answer, correct_answer="C", feedback=feedback)