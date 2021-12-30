import math
class filter_equations():

    def getXc(self, frequency, condensateur):
        return (1/(2* math.pi*2)*frequency*condensateur)

    def vout(self,vin,Xc,R):
        return vin*(Xc/(math.sqrt(math.pow(R,2))*(math.pow(Xc,2))))

    def logInverse(self, value):
        return math.pow(10,(value/20))

    def phasor_lower_pass(self,current_frequency,cutoff_frequency,transfer_function_factor):
        num_real = transfer_function_factor
        num_ima = -transfer_function_factor*(current_frequency/cutoff_frequency)
        denum = 1+(math.pow((current_frequency/cutoff_frequency),2))
        real = (num_real/denum)
        phasor_module = math.sqrt(math.pow(real,2)+math.pow(num_ima,2))
        phasor_phase = math.atan2(num_ima,real)
        return phasor_module, phasor_phase

    def lower_pass_bode(self,current_frequency,cutoff_frequency):
        return  1 / math.sqrt(1 + math.pow(current_frequency / cutoff_frequency, 2))

    def lower_pass_phase(self,current_frequency,cutoff_frequency):
        return -math.degrees(math.atan2(current_frequency,cutoff_frequency))

    def high_pass_phase(self,current_frequency,cutoff_frequency):
        return 90.0-math.degrees(math.atan2(current_frequency,cutoff_frequency))

    def high_pass_bode(self,current_frequency, cutoff_frequency):
        if(current_frequency/float(cutoff_frequency))/math.sqrt(1 + math.pow(current_frequency / float(cutoff_frequency), 2)) < 0:
            return 0
        else:
            return (current_frequency/float(cutoff_frequency))/math.sqrt(1 + math.pow(current_frequency / float(cutoff_frequency), 2))

    def band_pass_filter(self,current_frequency,cutoff_frequency,cutoff_frequency2):
        threshold = (cutoff_frequency2 + cutoff_frequency)/2
        if current_frequency >= threshold:
            return (current_frequency / cutoff_frequency) / math.sqrt(
                1 + math.pow(current_frequency / cutoff_frequency, 2))
        if current_frequency < threshold:
            return (current_frequency / cutoff_frequency) / math.sqrt(
                1 + math.pow(current_frequency / cutoff_frequency, 2))

    def log_time_20(self,impulsion):
        if(impulsion == 0):
            return -40
        return 20*math.log(impulsion,10)

    def routed_filter_convertion_from_bode_to_phase(self,proportioned_filter,current_frequency1, current_frequency2, filter_type,transfer_function):
        filter = self.find_filter(self,proportioned_filter.real_first_impulsion,proportioned_filter.real_last_impulsion,current_frequency1,current_frequency2,transfer_function,proportioned_filter)
        if "transfer_function" in str(type(filter)):
            cut_off = filter.cutoff1
        else:
            cut_off = filter.real_cut_off
        if filter_type == "passe bas routed":
            proportioned_filter.real_first_impulsion = self.log_time_20(self, self.lower_pass_bode(self, proportioned_filter.real_start_frequency, proportioned_filter.real_cut_off))
            proportioned_filter.real_last_impulsion = self.log_time_20(self, self.lower_pass_bode(self, proportioned_filter.real_end_frequency, proportioned_filter.real_cut_off))

            proportioned_filter.proportioned_impulsion_first = self.log_time_20(self, self.lower_pass_bode(self, current_frequency1, cut_off))
            proportioned_filter.proportioned_impulsion_last = self.log_time_20(self, self.lower_pass_bode(self, current_frequency2, cut_off))

            proportioned_filter.resolution_db = (proportioned_filter.real_first_impulsion  - proportioned_filter.real_last_impulsion) / (proportioned_filter.proportioned_impulsion_first - proportioned_filter.proportioned_impulsion_last)
            proportioned_filter.dephasing =  proportioned_filter.real_first_impulsion  /  proportioned_filter.resolution_db  - proportioned_filter.proportioned_impulsion_first
        elif filter_type == "passe haut routed":

            proportioned_filter.real_first_impulsion = 90.0 - math.degrees(
                math.atan2(proportioned_filter.real_start_frequency, proportioned_filter.real_cut_off))
            proportioned_filter.real_last_impulsion = 90.0 - math.degrees(
                math.atan2(proportioned_filter.real_end_frequency, proportioned_filter.real_cut_off))

            proportioned_filter.proportioned_impulsion_first = 90.0 - math.degrees(
                math.atan2(current_frequency1,cut_off))
            proportioned_filter.proportioned_impulsion_last = 90.0 - math.degrees(
                math.atan2(current_frequency2,cut_off))

            proportioned_filter.resolution_db = (proportioned_filter.real_first_impulsion - proportioned_filter.real_last_impulsion) / (
                                                            proportioned_filter.proportioned_impulsion_first - proportioned_filter.proportioned_impulsion_last)
            proportioned_filter.dephasing = proportioned_filter.real_first_impulsion / proportioned_filter.resolution_db - proportioned_filter.proportioned_impulsion_first
        return proportioned_filter

    def routed_filter_convertion_from_phase_to_bode(self,proportioned_filter,current_frequency1, current_frequency2, filter_type,transfer_function):
        filter = self.find_filter(self,proportioned_filter.real_first_impulsion,proportioned_filter.real_last_impulsion,current_frequency1,current_frequency2,transfer_function,proportioned_filter)
        if "transfer_function" in str(type(filter)):
            cut_off = filter.cutoff1
        else:
            cut_off = filter.real_cut_off
        if filter_type == "passe bas routed":
            proportioned_filter.real_first_impulsion = self.log_time_20(self, self.lower_pass_bode(self, proportioned_filter.real_start_frequency, proportioned_filter.real_cut_off))
            proportioned_filter.real_last_impulsion = self.log_time_20(self, self.lower_pass_bode(self, proportioned_filter.real_end_frequency, proportioned_filter.real_cut_off))

            proportioned_filter.proportioned_impulsion_first = self.log_time_20(self, self.lower_pass_bode(self, current_frequency1, cut_off))
            proportioned_filter.proportioned_impulsion_last = self.log_time_20(self, self.lower_pass_bode(self, current_frequency2, cut_off))

            proportioned_filter.resolution_db = (proportioned_filter.real_first_impulsion  - proportioned_filter.real_last_impulsion) / (proportioned_filter.proportioned_impulsion_first - proportioned_filter.proportioned_impulsion_last )
            proportioned_filter.dephasing =  proportioned_filter.real_first_impulsion  /  proportioned_filter.resolution_db  - proportioned_filter.proportioned_impulsion_first
        elif filter_type == "passe haut routed":
            proportioned_filter.real_first_impulsion = self.log_time_20(self, self.high_pass_bode(self, proportioned_filter.real_start_frequency, proportioned_filter.real_cut_off))
            proportioned_filter.real_last_impulsion = self.log_time_20(self, self.high_pass_bode(self, proportioned_filter.real_end_frequency, proportioned_filter.real_cut_off))

            proportioned_filter.proportioned_impulsion_first = self.log_time_20(self, self.high_pass_bode(self, current_frequency1, cut_off))
            proportioned_filter.proportioned_impulsion_last = self.log_time_20(self, self.high_pass_bode(self, current_frequency2, cut_off))
            proportioned_filter.resolution_db = (proportioned_filter.real_first_impulsion - proportioned_filter.real_last_impulsion) / (
                                                            proportioned_filter.proportioned_impulsion_first - proportioned_filter.proportioned_impulsion_last)
            proportioned_filter.dephasing = proportioned_filter.real_first_impulsion / proportioned_filter.resolution_db - proportioned_filter.proportioned_impulsion_first
        return proportioned_filter

    def get_phase_lower_pass(self,current_frequency, cutoff):
        return -1*math.degrees(math.atan2(current_frequency,cutoff))
    def get_phase_high_pass(self,current_frequency, cutoff):
        return 90.0 - math.degrees(math.atan2(current_frequency,cutoff))




