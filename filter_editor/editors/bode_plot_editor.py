from Waves.filter_editor.editors.plot_editor_calculator import plot_editor_calculator
from Waves.filter_editor.utilities.Equation_Maker import Equation_Maker
from Waves.filter_editor.utilities.filter_equations import *



class bode_plot_editor():

    def __init__(self, frequency_min, frequency_max, resolution, filter_fusion):
        self.name = "filter_editor_bode"
        self.filter_equations = filter_equations()
        self.frequency_min = frequency_min
        self.frequency_max = frequency_max
        self.resolution = resolution
        self.filter_fusion = filter_fusion
        self.freq = [0]*((self.frequency_max-self.frequency_min)*self.resolution)
        self.impulsion = [0]*((self.frequency_max-self.frequency_min)*self.resolution)
        self.plot_editor_calculator = plot_editor_calculator()

    def __plug__(self, editor):
        self.filter_equations = filter_equations()
        self.frequency_min = editor.frequency_min
        self.frequency_max = editor.frequency_max
        self.resolution = editor.resolution
        self.filter_fusion = editor.filter_fusion
        self.freq = editor.freq
        self.impulsion = editor.impulsion

    def __calculate_transfer_function__(self):
        if(self.name == "filter_editor_bode"):
            i = 0
            Equation_maker = Equation_Maker(self.filter_fusion)
            Equation_maker.__build_equation__()
            print(Equation_maker.string_equation)
            while i < len(self.filter_fusion.transfer_functions) :
                transfer_function = self.filter_fusion.transfer_functions[i];
                if self.filter_fusion.transfer_functions[i].type == "passe bas":
                    self.impulsion, self.freq = self.plot_editor_calculator.passe_bas_bode(transfer_function,filter_equations,self.resolution,self.impulsion,self.freq)
                if self.filter_fusion.transfer_functions[i].type == "passe haut":
                    self.impulsion, self.freq = self.plot_editor_calculator.passe_haut_bode(transfer_function,filter_equations,self.resolution,self.impulsion,self.freq)
                if self.filter_fusion.transfer_functions[i].proportioned_filter != None:
                    self.impulsion,self.freq = self.plot_editor_calculator.proportioned_filter_bode(self.filter_fusion.transfer_functions[i].proportioned_filter, self.impulsion, self.freq, self.resolution)
                i = i+1

    def __calculate_routed_filter__(self,proportion_filter,transfer_function):
        proportion_filter.dephasing,proportion_filter.real_start_frequency ,proportion_filter.real_end_frequency ,proportion_filter.resolution_frequency, proportion_filter.resolution_db , current_frequency1 , current_frequency2, proportion_filter.parent= \
            filter_equations.routed_filter_resolutions(filter_equations,
                                                       float(proportion_filter.real_cut_off),
                                                       float(proportion_filter.proportioned_impulsion_first),
                                                       float(proportion_filter.proportioned_impulsion_last),
                                                       float(proportion_filter.dephased_first_frequency),
                                                       float(proportion_filter.dephased_last_frequency),
                                                       float(proportion_filter.real_first_impulsion),
                                                       float(proportion_filter.real_last_impulsion),
                                                       proportion_filter.type,
                                                       transfer_function)
        if proportion_filter.dephased_first_frequency == -1:
            proportion_filter.dephased_first_frequency = current_frequency1
        if proportion_filter.dephased_last_frequency == -1:
            proportion_filter.dephased_last_frequency = current_frequency2
        return proportion_filter

    def __insert_transfer_function__(self,transfer_function_to_add):
        self.filter_fusion.__insert_transfer_function__(transfer_function_to_add)

    def __change_cutoff_1__(self, cutoff):
        self.filter_fusion.__change_cutoff_1__(cutoff)

    def __change_cutoff_2__(self, cutoff):
        self.filter_fusion.__change_cutoff_2__(cutoff)


    def __convert_resolution_to_frequency__(self,frequency,resolution):
        return frequency*resolution;

