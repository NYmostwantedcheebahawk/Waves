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

    def find_filter(self,impulsion_first,impulsion_last,dephased_first_frequency,dephased_last_frequency,transfer_function, comparable_value = None):
        for i in range(0,len(transfer_function)):
            value = None
            if transfer_function[i].proportioned_filter != None:
                for x in range(0,len(transfer_function[i].proportioned_filter)):
                    value = self.iterate_inside_filter(self, impulsion_first, impulsion_last, dephased_first_frequency,
                                          dephased_last_frequency, transfer_function[i].proportioned_filter[x])
                    if value == None:
                         value = self.find_curve_proportioned_filter(self,impulsion_first, impulsion_last, dephased_first_frequency,
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
                    value = self.find_curve_transfer_function(self,impulsion_first, impulsion_last, dephased_first_frequency,
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
                value = self.find_curve_transfer_function(self,impulsion_first, impulsion_last, dephased_first_frequency,
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
                value = self.iterate_inside_filter(self,impulsion_first,impulsion_last,dephased_first_frequency,dephased_last_frequency,proportioned_filter.proportioned_filters[x])
                if value == None:
                    return self.find_curve_proportioned_filter(self,impulsion_first, impulsion_last, dephased_first_frequency,
                                                   dephased_last_frequency, proportioned_filter.proportioned_filters[x])
                else:
                    return value
        else:
            return self.find_curve_proportioned_filter(self, impulsion_first, impulsion_last, dephased_first_frequency,
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

    def routed_filter_resolutions(self,cutoff,start_db,end_db,current_frequency1,current_frequency2,impulsion1,impulsion2,filter_type,transfer_function):
        filter = self.find_filter(self,impulsion1,impulsion2,current_frequency1,current_frequency2,transfer_function)
        if "transfer_function" in str(type(filter)):
            cut_off = filter.cutoff1
        else:
            cut_off = filter.real_cut_off

        if current_frequency1 == -1.0:
            if(filter.type == "passe haut routed"):
                if impulsion1 == 0:
                    current_frequency1 = (0.99 * cut_off) / (math.sqrt(1 - math.pow(0.99, 2)))
                    impulsion1 = self.log_time_20(self, self.high_pass_bode(self, current_frequency1, cut_off))
                else:
                    current_frequency1 = (self.logInverse(self, impulsion1) * cut_off) / (
                        math.sqrt(1 - math.pow(self.logInverse(self, impulsion1), 2)))
                    impulsion1 = self.log_time_20(self, self.high_pass_bode(self, current_frequency1, cut_off))
            elif(filter.type == "passe bas routed"):
                current_frequency1 = math.sqrt(math.pow((1/self.logInverse(self,impulsion1)),2)-1)*cut_off
                impulsion1 = self.log_time_20(self, self.lower_pass_bode(self, int(current_frequency1), cut_off))
            elif (filter.type == "passe bas"):
                current_frequency1 = math.sqrt(math.pow((1/self.logInverse(self,impulsion1)),2)-1)*cut_off
                impulsion1 = self.log_time_20(self, self.lower_pass_bode(self, int(current_frequency1), cut_off))

        if current_frequency2 == -1.0:
            if(filter.type == "passe haut routed"):
                if impulsion2 == 0:
                    current_frequency2 = (0.99 * 200) / (math.sqrt(1 - math.pow(0.99, 2)))
                    impulsion2 = self.log_time_20(self, self.high_pass_bode(self, current_frequency2, cut_off))
                else:
                    current_frequency2 = (self.logInverse(self, impulsion2) * cut_off) / (
                        math.sqrt(1 - math.pow(self.logInverse(self, impulsion2), 2)))
                    impulsion2 = self.log_time_20(self, self.high_pass_bode(self, current_frequency2, cut_off))
            elif(filter.type == "passe bas routed"):
                current_frequency2 = math.sqrt(math.pow((1/self.logInverse(self,impulsion2)),2)-1)*cut_off
                impulsion2 = self.log_time_20(self, self.lower_pass_bode(self, current_frequency2, cut_off))
            elif (filter.type == "passe bas"):
                current_frequency2 = math.sqrt(math.pow((1/self.logInverse(self,impulsion2)),2)-1)*cut_off
                impulsion2 = self.log_time_20(self, self.lower_pass_bode(self, current_frequency2, cut_off))


        if filter_type == "passe bas routed":
            real_start_frequency = math.sqrt(math.pow((1/self.logInverse(self,start_db)),2)-1)*cutoff
            real_end_frequency = math.sqrt(math.pow((1/self.logInverse(self,end_db)),2)-1)*cutoff

        elif filter_type == "passe haut routed":
            real_start_frequency = (self.logInverse(self,start_db)* cutoff)/(math.sqrt(1-math.pow(self.logInverse(self,start_db),2)))
            if end_db == 0:
                real_end_frequency = (0.99* cutoff)/(math.sqrt(1-math.pow(0.99,2)))
            else:
                real_end_frequency = (self.logInverse(self, end_db) * cutoff) / (
                    math.sqrt(1 - math.pow(self.logInverse(self, end_db), 2)))

        resolution_frequency = (real_end_frequency - real_start_frequency) / (current_frequency2 - current_frequency1)
        resolution_db = (start_db - end_db) / (impulsion1 - impulsion2)
        de_dephasing = start_db / resolution_db - impulsion1
        print(resolution_db)
        return de_dephasing,real_start_frequency, real_end_frequency, resolution_frequency, resolution_db, current_frequency1 ,current_frequency2,filter.priority

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




