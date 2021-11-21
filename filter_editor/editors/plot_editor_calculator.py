class plot_editor_calculator():
    def __init__(self):
       pass
    def proportioned_filter_bode(self, proportioned_filter,impulsion,freq,resolution):
        for x in range(0, len(proportioned_filter)):
            for e in range(int(proportioned_filter[x].dephased_first_frequency),int(proportioned_filter[x].dephased_last_frequency)):
                impulsion[e] = proportioned_filter[x].__get_impulsion__(e * resolution)
                freq[e] = self.__convert_resolution_to_frequency__(e, resolution)
            if proportioned_filter[x].proportioned_filters != None:
                impulsion,freq = self.proportioned_filter_bode(proportioned_filter[x].proportioned_filters,impulsion,freq,resolution)
        return impulsion, freq

    def passe_bas_bode(self,transfer_function,filter_equations,resolution,impulsion,freq):
        for x in range(transfer_function.frequency_min, (transfer_function.frequency_max * resolution)):
                filter_equations.lower_pass_bode(filter_equations, self.__convert_resolution_to_frequency__(0,
                                                                                                            resolution) ,
                                                 50)
                impulsion[x] = filter_equations.log_time_20(filter_equations,
                                                                 filter_equations.lower_pass_bode(filter_equations,
                                                                                                  self.__convert_resolution_to_frequency__(
                                                                                                      x,
                                                                                                      resolution) ,
                                                                                                  transfer_function.cutoff1))
                freq[x] = self.__convert_resolution_to_frequency__(x, resolution)
        return impulsion,freq

    def passe_haut_bode(self,transfer_function,filter_equations,resolution,impulsion,freq):
        for x in range(transfer_function.frequency_min,
                       (transfer_function.frequency_max * self.resolution)):
                impulsion[x] = filter_equations.log_time_20(filter_equations,
                                                                 filter_equations.high_pass_bode(filter_equations,
                                                                                                 self.__convert_resolution_to_frequency__(
                                                                                                     x,
                                                                                                     resolution) ,
                                                                                                 transfer_function.cutoff1))
                freq[x] = self.__convert_resolution_to_frequency__(x, resolution)

    def proportioned_filter_phase(self, proportioned_filter,impulsion,freq,resolution):
        for x in range(0, len(proportioned_filter)):
            for e in range(
                    int(proportioned_filter[x].dephased_first_frequency),
                    int(proportioned_filter[x].dephased_last_frequency)):
                impulsion[e] = proportioned_filter[x].__get_phase__(
                    e * resolution)
                freq[e] = self.__convert_resolution_to_frequency__(e, resolution)
            if proportioned_filter[x].proportioned_filters != None:
                impulsion,freq = self.proportioned_filter_phase(proportioned_filter[x].proportioned_filters,impulsion,freq,resolution)
        return impulsion,freq

    def passe_bas_phase(self,transfer_function,filter_equations,resolution,impulsion,freq):
        for x in range(transfer_function.frequency_min, (transfer_function.frequency_max * resolution)):

                filter_equations.lower_pass_bode(filter_equations, self.__convert_resolution_to_frequency__(0,
                                                                                                            resolution) ,
                                                 50)
                impulsion[x] = filter_equations.get_phase_lower_pass(filter_equations,
                                                                          self.__convert_resolution_to_frequency__(x,
                                                                                                                   resolution) ,
                                                                          transfer_function.cutoff1)
                freq[x] = self.__convert_resolution_to_frequency__(x, resolution)
        return impulsion, freq

    def passe_haut_phase(self,transfer_function,filter_equations,frequency_handicap,impulsion_handicap,resolution,impulsion,freq):
        for x in range(transfer_function.frequency_min,
                       (transfer_function.frequency_max * resolution)):
            modification_was_made = False
            if (transfer_function.manual_modifications != None):
                for o in range(0, len(transfer_function.manual_modifications)):
                    if transfer_function.manual_modifications[
                        o].starting_frequency <= self.__convert_resolution_to_frequency__(x, resolution) and \
                            transfer_function.manual_modifications[
                                o].last_frequency >= self.__convert_resolution_to_frequency__(x, resolution):
                        impulsion[x] = transfer_function.manual_modifications[o].impulsion_modification
                        freq[x] = self.__convert_resolution_to_frequency__(x, resolution)
                        modification_was_made = True
            if not modification_was_made:
                impulsion[x] = filter_equations.get_phase_high_pass(filter_equations,
                                                                         self.__convert_resolution_to_frequency__(x,
                                                                                                                  resolution) + frequency_handicap,
                                                                         transfer_function.cutoff1) + impulsion_handicap
                freq[x] = self.__convert_resolution_to_frequency__(x, resolution)

    def __convert_resolution_to_frequency__(self,frequency,resolution):
        return frequency*resolution;