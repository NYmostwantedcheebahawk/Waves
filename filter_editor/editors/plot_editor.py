from Waves.filter_editor.editors.bode_plot_editor import bode_plot_editor
from Waves.filter_editor.editors.phase_plot_editor import phase_plot_editor
from Waves.filter_editor.utilities import filter_fusion as ff
from Waves.filter_editor.utilities.Equation_Maker import Equation_Maker
from Waves.filter_editor.utilities.filter_equations import *
from Waves.filter_editor.utilities.proportioned_filter import proportioned_filter as pf
from Waves.filter_editor.utilities.transfert_function import transfer_function as transfer_function


class plot_editor():

    def __init__(self, state,frequency_min, frequency_max, resolution):
         new_transfer_function = transfer_function(200, None, 1, 1, 1, "passe bas", 0, None, 1000, None, None, None)
         filter_fusion = ff.filter_fusion(new_transfer_function)
         if (state == "Bode"):
             self.state = bode_plot_editor(frequency_min, frequency_max, resolution, filter_fusion)
         elif (state == "Phase"):
             self.state = phase_plot_editor(frequency_min, frequency_max, resolution, filter_fusion)
         self.priority = 0

    def __get_equation__(self):
        result = Equation_Maker(self.state.filter_fusion)
        result.__build_equation__()
        return result.string_equation

    def __add_routed_filter__(self,proportioned_impulsion_first, proportioned_impulsion_last, real_first_impulsion,real_last_impulsion, routed_filter_type, dephased_first_frequency, dephased_last_frequency,real_cut_off,periodic_frequency,relativeOrAbsolute,pattern,attached,proportioned_filter = None):
         new_proportioned_filter = pf(float(proportioned_impulsion_first), float(proportioned_impulsion_last),float(real_first_impulsion), float(real_last_impulsion), routed_filter_type,float(dephased_first_frequency), float(dephased_last_frequency), float(real_cut_off),periodic_frequency, relativeOrAbsolute, pattern, attached)
         self.priority  = self.priority +1
         filter = self.state.find_filter(new_proportioned_filter.real_first_impulsion,new_proportioned_filter.real_first_impulsion,new_proportioned_filter.dephased_first_frequency,new_proportioned_filter.dephased_last_frequency,self.state.filter_fusion.transfer_functions)
         new_proportioned_filter = self.__calculate_routed_filter__(new_proportioned_filter,self.state.filter_fusion.transfer_functions)
         new_proportioned_filter.priority = self.priority
         filter.__insert_proportioned_filter__(new_proportioned_filter)
         i1 = 0
         if "routed" not in filter.type:
             if "bas" in filter.type:
                 i1 = filter_equations.log_time_20(filter_equations, filter_equations.lower_pass_bode(filter_equations,
                                                                                                      new_proportioned_filter.dephased_last_frequency,
                                                                                                      filter.cutoff1))
             elif "haut" in filter.type:
                 i1 = filter_equations.log_time_20(filter_equations, filter_equations.high_pass_bode(filter_equations,
                                                                                                     new_proportioned_filter.dephased_last_frequency,
                                                                                                     filter.cutoff1))
         else:
             i1 = filter.__get_impulsion__(new_proportioned_filter.dephased_last_frequency)

         new_proportioned_filter.attached_to_parent = (new_proportioned_filter.real_last_impulsion == i1)
         self.__calculate_transfer_function__()

    def __add_filter__(self,cutoff1, cutoff2, order, resolution, resolutiondb, type, frequency_min, frequency_middle ,frequency_max, impulsion_first, impulsion_middle, impulsion_last):
        transfer_function_to_add = transfer_function(cutoff1, cutoff2, order, resolution, resolutiondb, type,frequency_min, frequency_middle, frequency_max, impulsion_first,impulsion_middle, impulsion_last, None)
        self.state.__insert_transfer_function__(transfer_function_to_add)
        self.state.__calculate_transfer_function__()

    def __calculate_transfer_function__(self):
        self.state.__calculate_transfer_function__()

    def __calculate_routed_filter__(self,proportion_filter,transfer_function):
        return self.state.__calculate_routed_filter__(proportion_filter,transfer_function)

    def __change_cutoff_1__(self, cutoff):
        self.state.__change_cutoff_1__(cutoff)

    def __change_cutoff_2__(self, cutoff):
        self.state.__change_cutoff_2__(cutoff)

    def __find_transfer_functions_affected_by_modification__(self, first, last):
        self.state.__find_transfer_functions_affected_by_modification__(first, last)

    def __convert_resolution_to_frequency__(self,frequency,resolution):
        self.state.__convert_resolution_to_frequency__(frequency,resolution)

    def __change_state__(self,state):
        if(state == "Bode"):
            interState = self.state
            self.state = bode_plot_editor(0, 0, 0, 0)
            self.state.__plug__(interState)
            i = 0
            while i < len(self.state.filter_fusion.transfer_functions):
                transfer_function = self.state.filter_fusion.transfer_functions[i];
                if transfer_function.proportioned_filter != None:
                    for x in range(0, len(transfer_function.proportioned_filter)):
                        self.state.filter_fusion.transfer_functions[i].proportioned_filter[x] = filter_equations.routed_filter_convertion_from_phase_to_bode(filter_equations, transfer_function.proportioned_filter[x],
                                                                                                                                                             transfer_function.proportioned_filter[x].dephased_first_frequency,
                                                                                                                                                             transfer_function.proportioned_filter[x].dephased_last_frequency, transfer_function.proportioned_filter[x].type, self.state.filter_fusion.transfer_functions)
                i = i+1
        elif(state == "Phase"):
            interState = self.state
            self.state = phase_plot_editor(0, 0, 0, 0)
            self.state.__plug__(interState)
            i = 0

            while i < len(self.state.filter_fusion.transfer_functions):
                transfer_function = self.state.filter_fusion.transfer_functions[i];
                if transfer_function.proportioned_filter != None:
                    for x in range(0, len(transfer_function.proportioned_filter)):
                        self.state.filter_fusion.transfer_functions[i].proportioned_filter[x] = filter_equations.routed_filter_convertion_from_bode_to_phase(filter_equations, transfer_function.proportioned_filter[x],
                                                                                                                                                             transfer_function.proportioned_filter[x].dephased_first_frequency,
                                                                                                                                                             transfer_function.proportioned_filter[x].dephased_last_frequency, transfer_function.proportioned_filter[x].type, self.state.filter_fusion.transfer_functions)
                i = i+1