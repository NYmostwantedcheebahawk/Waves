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
        proportion_filter = self.routed_filter_resolutions(proportion_filter,transfer_function)
        return proportion_filter

    def __insert_transfer_function__(self,transfer_function_to_add):
        self.filter_fusion.__insert_transfer_function__(transfer_function_to_add)

    def __change_cutoff_1__(self, cutoff):
        self.filter_fusion.__change_cutoff_1__(cutoff)

    def __change_cutoff_2__(self, cutoff):
        self.filter_fusion.__change_cutoff_2__(cutoff)


    def __convert_resolution_to_frequency__(self,frequency,resolution):
        return frequency*resolution;

    def routed_filter_resolutions(self,proportion_filter,transfer_function):
        filter = self.find_filter(float(proportion_filter.real_first_impulsion),float(proportion_filter.real_last_impulsion),float(proportion_filter.dephased_first_frequency),float(proportion_filter.dephased_last_frequency),transfer_function)
        if "transfer_function" in str(type(filter)):
            cut_off = filter.cutoff1
        else:
            cut_off = filter.real_cut_off

        if float(proportion_filter.dephased_first_frequency) == -1.0:
            if(filter.type == "passe haut routed"):
                if float(proportion_filter.real_first_impulsion) == 0:
                    proportion_filter.dephased_first_frequency = (0.99 * cut_off) / (math.sqrt(1 - math.pow(0.99, 2)))
                    proportion_filter.real_first_impulsion = self.filter_equations.log_time_20(self.filter_equations.high_pass_bode(float(proportion_filter.dephased_first_frequency), cut_off))
                else:
                    proportion_filter.dephased_first_frequency = (self.filter_equations.logInverse(float(proportion_filter.real_first_impulsion)) * cut_off) / (
                        math.sqrt(1 - math.pow(self.filter_equations.logInverse(float(proportion_filter.real_first_impulsion)), 2)))
                    proportion_filter.real_first_impulsion = self.filter_equations.log_time_20(self.filter_equations.high_pass_bode(float(proportion_filter.dephased_first_frequency), cut_off))
            elif(filter.type == "passe bas routed"):
                proportion_filter.dephased_first_frequency = math.sqrt(math.pow((1/self.filter_equations.logInverse(float(proportion_filter.real_first_impulsion))),2)-1)*cut_off
                proportion_filter.real_first_impulsion = self.filter_equations.log_time_20(self.filter_equations.lower_pass_bode( float(proportion_filter.dephased_first_frequency), cut_off))
            elif (filter.type == "passe bas"):
                proportion_filter.dephased_first_frequency = math.sqrt(math.pow((1/self.filter_equations.logInverse(float(proportion_filter.real_first_impulsion))),2)-1)*cut_off
                proportion_filter.real_first_impulsion = self.filter_equations.log_time_20(self.filter_equations.lower_pass_bode( float(proportion_filter.dephased_first_frequency), cut_off))

        if float(proportion_filter.dephased_last_frequency) == -1.0:
            if(filter.type == "passe haut routed"):
                if float(proportion_filter.real_last_impulsion) == 0:
                    proportion_filter.dephased_last_frequency = (0.99 * 200) / (math.sqrt(1 - math.pow(0.99, 2)))
                    proportion_filter.real_last_impulsion = self.filter_equations.log_time_20(self.filter_equations.high_pass_bode( float(proportion_filter.dephased_last_frequency), cut_off))
                else:
                    proportion_filter.dephased_last_frequency = (self.filter_equations.logInverse(float(proportion_filter.real_last_impulsion)) * cut_off) / (
                        math.sqrt(1 - math.pow(self.filter_equations.logInverse(float(proportion_filter.real_last_impulsion)), 2)))
                    proportion_filter.real_last_impulsion = self.filter_equations.log_time_20(self.filter_equations.high_pass_bode(float(proportion_filter.dephased_last_frequency), cut_off))
            elif(filter.type == "passe bas routed"):
                proportion_filter.dephased_last_frequency = math.sqrt(math.pow((1/self.filter_equations.logInverse(float(proportion_filter.real_last_impulsion))),2)-1)*cut_off
                proportion_filter.real_last_impulsion = self.filter_equations.log_time_20(self.filter_equations.lower_pass_bode(float(proportion_filter.dephased_last_frequency), cut_off))
            elif (filter.type == "passe bas"):
                proportion_filter.dephased_last_frequency = math.sqrt(math.pow((1/self.filter_equations.logInverse(float(proportion_filter.real_last_impulsion))),2)-1)*cut_off
                proportion_filter.real_last_impulsion = self.filter_equations.log_time_20(self.filter_equations.lower_pass_bode(float(proportion_filter.dephased_last_frequency), cut_off))


        if proportion_filter.type == "passe bas routed":
            proportion_filter.real_start_frequency  = math.sqrt(math.pow((1/self.filter_equations.logInverse(float(proportion_filter.proportioned_impulsion_first))),2)-1)*float(proportion_filter.real_cut_off)
            proportion_filter.real_end_frequency = math.sqrt(math.pow((1/self.filter_equations.logInverse(float(proportion_filter.proportioned_impulsion_last))),2)-1)*float(proportion_filter.real_cut_off)

        elif proportion_filter.type == "passe haut routed":
            proportion_filter.real_start_frequency  = (self.filter_equations.logInverse(float(proportion_filter.proportioned_impulsion_first))* float(proportion_filter.real_cut_off))/(math.sqrt(1-math.pow(self.filter_equations.logInverse(float(proportion_filter.proportioned_impulsion_first)),2)))
            if float(proportion_filter.proportioned_impulsion_last) == 0:
                proportion_filter.real_end_frequency = (0.99* float(proportion_filter.real_cut_off))/(math.sqrt(1-math.pow(0.99,2)))
            else:
                proportion_filter.real_end_frequency = (self.filter_equations.logInverse(float(proportion_filter.proportioned_impulsion_last)) * float(proportion_filter.real_cut_off)) / (
                    math.sqrt(1 - math.pow(self.filter_equations.logInverse(float(proportion_filter.proportioned_impulsion_last)), 2)))

        proportion_filter.resolution_frequency = (proportion_filter.real_end_frequency - proportion_filter.real_start_frequency ) / (float(proportion_filter.dephased_last_frequency) - float(proportion_filter.dephased_first_frequency))
        proportion_filter.resolution_db = (float(proportion_filter.proportioned_impulsion_first) - float(proportion_filter.proportioned_impulsion_last)) / (float(proportion_filter.real_first_impulsion) - float(proportion_filter.real_last_impulsion))
        proportion_filter.dephasing = float(proportion_filter.proportioned_impulsion_first) / proportion_filter.resolution_db - float(proportion_filter.real_first_impulsion)
        print(proportion_filter.resolution_db)
        return proportion_filter

    def find_filter(self,impulsion_first,impulsion_last,dephased_first_frequency,dephased_last_frequency,transfer_function, comparable_value = None):
        for i in range(0,len(transfer_function)):
            value = None
            if transfer_function[i].proportioned_filter != None:
                for x in range(0,len(transfer_function[i].proportioned_filter)):
                    value = self.iterate_inside_filter(impulsion_first, impulsion_last, dephased_first_frequency,
                                          dephased_last_frequency, transfer_function[i].proportioned_filter[x])
                    if value == None:
                         value = self.find_curve_proportioned_filter(impulsion_first, impulsion_last, dephased_first_frequency,
                                                            dephased_last_frequency, transfer_function[i].proportioned_filter[x])
                    if(value != None):
                        if(comparable_value == None):
                            pass
                        else:
                            if(comparable_value != value):
                                pass
                            else:
                                value = transfer_function[i]
                if value == None:
                    value = self.find_curve_transfer_function(impulsion_first, impulsion_last, dephased_first_frequency,
                                                        dephased_last_frequency,
                                                        transfer_function[i])
                if(value != None):
                    if (comparable_value == None):
                        pass
                    else:
                        if (comparable_value != value):
                            pass
                        else:
                            value = None

            else:
                value = self.find_curve_transfer_function(impulsion_first, impulsion_last, dephased_first_frequency,
                                                          dephased_last_frequency,
                                                          transfer_function[i])
                if (value != None):
                    if (comparable_value == None):
                        pass
                    else:
                        if (comparable_value != value):
                            pass
                        else:
                            value = None
        return value

    def find_curve_transfer_function(self,impulsion_first,impulsion_last,dephased_first_frequency,dephased_last_frequency,transfer_function):
        found = True
        if impulsion_last > impulsion_first:
            if transfer_function.impulsion_first  > transfer_function.impulsion_last:
                if transfer_function.impulsion_first  < impulsion_last:
                    found = False
                if transfer_function.impulsion_last > impulsion_first:
                    found = False
            else:
                if transfer_function.impulsion_last < impulsion_last:
                    found = False
                if transfer_function.impulsion_first  > impulsion_first:
                    found = False
        else:
            if transfer_function.impulsion_first  > transfer_function.impulsion_last:
                if transfer_function.impulsion_first  < impulsion_first:
                    found = False
                if transfer_function.impulsion_last > impulsion_last:
                    found = False
            else:
                if transfer_function.impulsion_last < impulsion_first:
                    found = False
                if transfer_function.impulsion_first  > impulsion_last:
                    found = False
        # check if none
        if dephased_first_frequency != -1.0:
            if(transfer_function.frequency_min > dephased_first_frequency):
                found = False
        # check if none
        if dephased_last_frequency != -1.0:
            if(transfer_function.frequency_max < dephased_last_frequency):
                found = False
        if found:
            return transfer_function
        else:
            return None

    def iterate_inside_filter(self, impulsion_first,impulsion_last,dephased_first_frequency,dephased_last_frequency,proportioned_filter,):
        if proportioned_filter.proportioned_filters != None:
            for x in range(0, len(proportioned_filter.proportioned_filters)):
                value = self.iterate_inside_filter(impulsion_first,impulsion_last,dephased_first_frequency,dephased_last_frequency,proportioned_filter.proportioned_filters[x])
                if value == None:
                    return self.find_curve_proportioned_filter(impulsion_first, impulsion_last, dephased_first_frequency,
                                                   dephased_last_frequency, proportioned_filter.proportioned_filters[x])
                else:
                    return value
        else:
            return self.find_curve_proportioned_filter(impulsion_first, impulsion_last, dephased_first_frequency,
                                                       dephased_last_frequency, proportioned_filter)

    def find_curve_proportioned_filter(self,impulsion_first,impulsion_last,dephased_first_frequency,dephased_last_frequency,proportioned_filter):
        found = True

        if impulsion_last > impulsion_first:
            if proportioned_filter.real_first_impulsion > proportioned_filter.real_last_impulsion:
                if proportioned_filter.real_first_impulsion < impulsion_last:
                    found = False
                if proportioned_filter.real_last_impulsion > impulsion_first:
                    found = False
            else:
                if proportioned_filter.real_last_impulsion < impulsion_last:
                    found = False
                if proportioned_filter.real_first_impulsion > impulsion_first:
                    found = False
        else:
            if proportioned_filter.real_first_impulsion > proportioned_filter.real_last_impulsion:
                if proportioned_filter.real_first_impulsion < impulsion_first:
                    found = False
                if proportioned_filter.real_last_impulsion > impulsion_last:
                    found = False
            else:
                if proportioned_filter.real_last_impulsion < impulsion_first:
                    found = False
                if proportioned_filter.real_first_impulsion > impulsion_last:
                    found = False
        # check if none
        if dephased_first_frequency != -1.0:
            if(proportioned_filter.dephased_first_frequency > dephased_first_frequency):
                found = False
            if(proportioned_filter.dephased_last_frequency <= dephased_first_frequency):
                found = False
        # check if none
        if dephased_last_frequency != -1.0:
            if(proportioned_filter.dephased_last_frequency < dephased_last_frequency):
                found = False
            if(proportioned_filter.dephased_first_frequency >= dephased_last_frequency):
                found = False
        if found:
            return proportioned_filter
        else:
            return None