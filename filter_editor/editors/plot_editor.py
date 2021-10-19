from Waves.filter_editor.editors.bode_plot_editor import bode_plot_editor
from Waves.filter_editor.editors.phase_plot_editor import phase_plot_editor
import math
from Waves.filter_editor.utilities.filter_equations import *
from Waves.filter_editor.utilities.transfert_function import transfer_function as transfer_function


class plot_editor():

    def __init__(self, state,frequency_min, frequency_max, resolution, filter_fusion):
        if(state == "Bode"):
            self.state = bode_plot_editor(frequency_min, frequency_max, resolution, filter_fusion)
        elif(state == "Phase"):
            self.state = phase_plot_editor(frequency_min, frequency_max, resolution, filter_fusion)

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
                        self.state.filter_fusion.transfer_functions[i].proportioned_filter[x] = filter_equations.routed_filter_convertion_from_phase_to_bode(filter_equations,transfer_function.proportioned_filter[x],
                            transfer_function.proportioned_filter[x].dephased_first_frequency,
                            transfer_function.proportioned_filter[x].dephased_last_frequency, transfer_function.proportioned_filter[x].routed_filter_type,self.state.filter_fusion.transfer_functions)
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
                        self.state.filter_fusion.transfer_functions[i].proportioned_filter[x] = filter_equations.routed_filter_convertion_from_bode_to_phase(filter_equations,transfer_function.proportioned_filter[x],
                            transfer_function.proportioned_filter[x].dephased_first_frequency,
                            transfer_function.proportioned_filter[x].dephased_last_frequency, transfer_function.proportioned_filter[x].routed_filter_type,self.state.filter_fusion.transfer_functions)
                i = i+1