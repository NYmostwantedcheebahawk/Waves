import math

from Waves.filter_editor.utilities.filter_equations import filter_equations


class proportioned_filter():
    def __init__(self,proportioned_impulsion_first, proportioned_impulsion_last, real_first_impulsion,
                 real_last_impulsion, routed_filter_type, dephased_first_frequency, dephased_last_frequency,
                 real_cut_off,periodic_frequency,relativeOrAbsolute,pattern,attached,proportioned_filter = None):
        self.proportioned_impulsion_first = proportioned_impulsion_first
        self.proportioned_impulsion_last = proportioned_impulsion_last
        self.real_first_impulsion = real_first_impulsion
        self.real_last_impulsion = real_last_impulsion
        self.type = routed_filter_type
        self.dephased_first_frequency = dephased_first_frequency
        self.dephased_last_frequency = dephased_last_frequency
        self.real_cut_off = real_cut_off
        self.priority = 0
        self.parent = 0
        if(dephased_first_frequency == -1.0):
            self.start_frequency_connected = True
        else:
            self.start_frequency_connected = False
        if(dephased_last_frequency == -1.0):
            self.end_frequency_connected = True
        else:
            self.end_frequency_connected = False
        self.real_start_frequency = 0
        self.real_end_frequency = 0
        self.resolution_frequency = 0
        self.resolution_db = 0
        self.dephasing = 0
        self.periodic_frequency = periodic_frequency
        self.pattern = pattern
        self.attached = attached
        self.relativeOrAbsolute = relativeOrAbsolute
        self.attached_to_parent = False


        if (proportioned_filter != None):
            self.proportioned_filters = [proportioned_filter]
        else:
            self.proportioned_filters= None

    def __get_impulsion__(self,current_frequency):

        if(self.type == "passe bas routed"):
            return filter_equations.log_time_20(filter_equations,
                                     filter_equations.lower_pass_bode(
                                         filter_equations,
                                         (current_frequency - self.dephased_first_frequency) * self.resolution_frequency
                                         + self.real_start_frequency,
                                         self.real_cut_off)) / self.resolution_db - float(
            self.dephasing)
        if (self.type == "passe haut routed"):
            return filter_equations.log_time_20(filter_equations,
                                                filter_equations.high_pass_bode(
                                                filter_equations,
                                                (current_frequency - self.dephased_first_frequency)
                                                *self.resolution_frequency +
                                                self.real_start_frequency,
                                                self.real_cut_off)) / self.resolution_db - float(self.dephasing)

    def __get_phase__(self,current_frequency):
        if(self.type == "passe bas routed"):
            return filter_equations.get_phase_lower_pass(filter_equations,(current_frequency- self.dephased_first_frequency)* self.resolution_frequency + self.real_start_frequency,self.real_cut_off)/self.resolution_db - float(self.dephasing)

        elif(self.type == "passe haut routed"):
            return filter_equations.get_phase_high_pass(filter_equations,(float(current_frequency)- float(self.dephased_first_frequency))* self.resolution_frequency + self.real_start_frequency,self.real_cut_off)/self.resolution_db - float(self.dephasing)


    def __convert_resolution_to_frequency__(self, frequency, resolution):
            return frequency * resolution;

    def __insert_proportioned_filter__(self,proportioned_filter):
        if(self.proportioned_filters == None):
            self.proportioned_filters = [proportioned_filter]
        else:
            self.proportioned_filters.insert(-1, proportioned_filter)
    


