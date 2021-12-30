import math

from Waves.filter_editor.utilities.filter_equations import filter_equations
class proportioned_filter_equation():
    def __init__(self,dephased_first_frequency,dephased_last_frequency,proportioned_impulsion_first,proportioned_impulsion_last,real_first_impulsion,real_last_impulsion,routed_filter,resolution_frequency,real_start_frequency,real_end_frequency,real_cut_off,resolution_db, dephasing ,priority,attached,relativeOrAbsolute,parent_cut_off,parent,attachment_to_parent):
        self.dephased_first_frequency =float (dephased_first_frequency)
        self.dephased_last_frequency =float (dephased_last_frequency)
        self.proportioned_impulsion_first =float (proportioned_impulsion_first)
        self.proportioned_impulsion_last =float (proportioned_impulsion_last)
        self.real_first_impulsion =float (real_first_impulsion)
        self.real_last_impulsion =float (real_last_impulsion)
        self.type = routed_filter
        self.resolution_frequency =float (resolution_frequency)
        self.real_start_frequency =float (real_start_frequency)
        self.real_end_frequency =float (real_end_frequency)
        self.real_cut_off =float (real_cut_off)
        self.parent_cut_off =float (parent_cut_off)
        self.resolution_db =float (resolution_db)
        self.dephasing =float (dephasing)
        self.priority =int(priority)
        self.attached =attached
        self.relativeOrAbsolute =relativeOrAbsolute
        self.parent = int(parent)
        self.attached_to_parent = attachment_to_parent
        self.difference = self.real_last_impulsion - self.real_first_impulsion
        self.activated = True;

    def __get_impulsion__(self, current_frequency):
        if (self.type == "passe bas routed"):
            return filter_equations.log_time_20(filter_equations,
                                                filter_equations.lower_pass_bode(
                                                    filter_equations,
                                                    (current_frequency - self.dephased_first_frequency)
                                                    * self.resolution_frequency +
                                                    self.real_start_frequency,
                                                    self.real_cut_off)) / self.resolution_db - self.dephasing
        if (self.type == "passe haut routed"):
            return filter_equations.log_time_20(filter_equations,
                                                filter_equations.high_pass_bode(
                                                    filter_equations,
                                                    (current_frequency - self.dephased_first_frequency)
                                                    * self.resolution_frequency +
                                                    self.real_start_frequency,
                                                    self.real_cut_off)) / self.resolution_db - self.dephasing


    def __convert_resolution_to_frequency__(self, frequency, resolution):
            return frequency * resolution;

    def __get_last_frequency__(self):
        return self.dephased_last_frequency

    def routed_filter_resolutions(self,impulsion,filter):
        if self.attached_to_parent == 'True':
            if self.type == "passe haut routed":
                if impulsion == None:
                    if filter.type == "lower_pass" or filter.type == "passe bas routed":
                        impulsion1 = filter_equations.log_time_20(filter_equations, filter_equations.lower_pass_bode(self, self.dephased_first_frequency, self.parent_cut_off))
                    elif filter.type == "high_pass" or filter.type == "passe haut routed":
                        impulsion1 = filter_equations.log_time_20(filter_equations, filter_equations.high_pass_bode(self,self.dephased_first_frequency,self.parent_cut_off))
                else:
                    impulsion1 = impulsion
                if self.relativeOrAbsolute == "relative":
                   impulsion2 = (self.real_last_impulsion - self.real_first_impulsion) + impulsion1
                   self.real_first_impulsion = impulsion1
                   self.real_last_impulsion = impulsion2

                elif self.relativeOrAbsolute == "absolute":
                   self.real_first_impulsion = impulsion1

                self.resolution_db = (self.proportioned_impulsion_first-self.proportioned_impulsion_last)/(self.real_first_impulsion-self.real_last_impulsion)
                self.dephasing = self.proportioned_impulsion_first/self.resolution_db - self.real_first_impulsion


            elif self.type == "passe bas routed":
                if filter.type == "lower_pass" or filter.type == "passe bas routed":
                    impulsion2 = filter_equations.log_time_20(filter_equations, filter_equations.lower_pass_bode(self,self.dephased_last_frequency,self.parent_cut_off))
                elif filter.type == "high_pass" or filter.type == "passe haut routed":
                    impulsion2 = filter_equations.log_time_20(filter_equations, filter_equations.high_pass_bode(self,self.dephased_last_frequency,self.parent_cut_off))

                if self.relativeOrAbsolute == "relative":
                    impulsion1 = (self.real_first_impulsion - self.real_last_impulsion) + impulsion2
                    if impulsion == None:
                        self.real_first_impulsion = impulsion1
                    else:
                        self.real_first_impulsion = impulsion
                    self.real_last_impulsion = impulsion2

                elif self.relativeOrAbsolute == "absolute":
                    self.real_last_impulsion = impulsion2

                self.resolution_db = (self.proportioned_impulsion_first - self.proportioned_impulsion_last) / (self.real_first_impulsion - self.real_last_impulsion)
                self.dephasing = self.proportioned_impulsion_last / self.resolution_db - self.real_last_impulsion
        else:
            if impulsion == None:
                if filter.type == "lower_pass" or filter.type == "passe bas routed":
                    impulsion1 = filter_equations.log_time_20(filter_equations, filter_equations.lower_pass_bode(self,
                                                                                                                 self.dephased_first_frequency,
                                                                                                                 self.parent_cut_off))
                elif filter.type == "high_pass" or filter.type == "passe haut routed":
                    impulsion1 = filter_equations.log_time_20(filter_equations, filter_equations.high_pass_bode(self,
                                                                                                                self.dephased_first_frequency,
                                                                                                                self.parent_cut_off))
            else:
                impulsion1 = impulsion
            if self.relativeOrAbsolute == "relative":
                impulsion2 = self.difference +  impulsion1
                self.real_first_impulsion = impulsion1
                self.real_last_impulsion = impulsion2

            elif self.relativeOrAbsolute == "absolute":
                self.real_first_impulsion = impulsion1

            self.resolution_db = (self.proportioned_impulsion_first - self.proportioned_impulsion_last) / (
                        self.real_first_impulsion - self.real_last_impulsion)
            self.dephasing = self.proportioned_impulsion_first / self.resolution_db - self.real_first_impulsion


    def __update__(self,frequency1,frequency2,impulsion,filter):
        self.dephased_first_frequency = frequency1
        self.dephased_last_frequency = frequency2
        if self.attached == "yes":
            self.routed_filter_resolutions(impulsion,filter)








