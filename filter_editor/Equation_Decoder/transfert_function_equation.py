import math

from Waves.filter_editor.utilities.filter_equations import filter_equations


class tranfert_function_equation():
    def __init__(self,cut_off,type):
        self.cutoff = cut_off
        self.type = type
        self.priority = 0

    def __get_impulsion__(self,current_frequency):
        if self.type == "lower_pass":
            return self.__lower_pass_bode__(current_frequency)
        elif self.type == "high_pass":
            return self.__high_pass_bode__(current_frequency)

    def __lower_pass_bode__(self,current_frequency):
        return filter_equations.log_time_20(filter_equations,1 / math.sqrt(1 + math.pow(current_frequency / float(self.cutoff), 2)))

    def __high_pass_bode__(self,current_frequency):
        return filter_equations.log_time_20(filter_equations,(current_frequency/float(self.cutoff))/math.sqrt(1 + math.pow(current_frequency / float(self.cutoff), 2)))

    def __get_last_frequency__(self):
        return "check_frequency"

    def __update__(self):
        pass