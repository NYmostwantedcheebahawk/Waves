class Equation_Maker():
    def __init__(self,filter_fusion):
        self.filter_fusion = filter_fusion
        self.string_equation = ""

    def __add_low_pass_filter__(self,cut_off):
        if self.string_equation == "":
            self.string_equation = self.string_equation + "low_pass_filter" + "("+str(cut_off)+")"
        else:
            self.string_equation = self.string_equation + "+low_pass_filter" + "(" + str(cut_off) + ")"

    def __add_high_pass_filter__(self,cut_off):
        if self.string_equation == "":
            self.string_equation = self.string_equation + "high_pass_filter"+ "("+str(cut_off)+")"
        else:
            self.string_equation = self.string_equation + "+high_pass_filter" + "(" + str(cut_off) + ")"

    def __add_routed_low_pass_filter__(self,proportioned_filter,parent_cut_off):
        if self.string_equation == "":
            self.string_equation = self.string_equation + "routed_low_pass_filter" + "(" + str(
                proportioned_filter.dephased_first_frequency) + "," + str(
                proportioned_filter.dephased_last_frequency) + "," + str(
                proportioned_filter.proportioned_impulsion_first) + "," + str(
                proportioned_filter.proportioned_impulsion_last) + "," + str(
                proportioned_filter.real_first_impulsion) + "," + str(
                proportioned_filter.real_last_impulsion) + "," + str(
                proportioned_filter.type) + "," + str(
                proportioned_filter.resolution_frequency) + "," + str(
                proportioned_filter.real_start_frequency) + "," + str(proportioned_filter.real_cut_off) + "," + str(
                proportioned_filter.resolution_db) + "," + str(proportioned_filter.dephasing) + "," + str(
                proportioned_filter.priority) + "," + str(proportioned_filter.attached) + "," + str(
                proportioned_filter.relativeOrAbsolute) + "," + str(parent_cut_off) + "," +str(proportioned_filter.parent)+ "," + str(proportioned_filter.attached_to_parent) + ")"

        else:
            self.string_equation = self.string_equation + "+routed_low_pass_filter" + "(" + str(
                proportioned_filter.dephased_first_frequency) + "," + str(
                proportioned_filter.dephased_last_frequency) + "," + str(
                proportioned_filter.proportioned_impulsion_first) + "," + str(
                proportioned_filter.proportioned_impulsion_last) + "," + str(
                proportioned_filter.real_first_impulsion) + "," + str(
                proportioned_filter.real_last_impulsion) + "," + str(
                proportioned_filter.type) + "," + str(
                proportioned_filter.resolution_frequency) + "," + str(
                proportioned_filter.real_start_frequency) + "," + str(
                proportioned_filter.real_end_frequency) + "," + str(proportioned_filter.real_cut_off) + "," + str(
                proportioned_filter.resolution_db) + "," + str(proportioned_filter.dephasing) + "," + str(
                proportioned_filter.priority) + "," + str(proportioned_filter.attached) + "," + str(
                proportioned_filter.relativeOrAbsolute) + "," + str(parent_cut_off) + "," + str(proportioned_filter.parent)+ ","+ str(proportioned_filter.attached_to_parent) + ")"
    def __add_routed_high_pass_filter__(self,proportioned_filter,parent_cut_off):
        if self.string_equation == "":
            self.string_equation = self.string_equation + "routed_high_pass_filter" + "(" + str(
                proportioned_filter.dephased_first_frequency) + "," + str(
                proportioned_filter.dephased_last_frequency) + "," + str(
                proportioned_filter.proportioned_impulsion_first) + "," + str(
                proportioned_filter.proportioned_impulsion_last) + "," + str(
                proportioned_filter.real_first_impulsion) + "," + str(
                proportioned_filter.real_last_impulsion) + "," + str(
                proportioned_filter.type) + "," + str(
                proportioned_filter.resolution_frequency) + "," + str(
                proportioned_filter.real_start_frequency) + "," + str(
                proportioned_filter.real_cut_off) + "," + str(
                proportioned_filter.resolution_db) + "," + str(
                proportioned_filter.dephasing) + "," + str(
                proportioned_filter.priority) + "," + str(
                proportioned_filter.attached) + "," + str(
                proportioned_filter.relativeOrAbsolute) + "," + str(
                parent_cut_off)+ "," +str(
                proportioned_filter.parent)+ "," + str(
                proportioned_filter.attached_to_parent) + ")"

        else:
            self.string_equation = self.string_equation + "+routed_high_pass_filter" + "(" + str(
                proportioned_filter.dephased_first_frequency) + "," + str(
                proportioned_filter.dephased_last_frequency) + "," + str(
                proportioned_filter.proportioned_impulsion_first) + "," + str(
                proportioned_filter.proportioned_impulsion_last) + "," + str(
                proportioned_filter.real_first_impulsion) + "," + str(
                proportioned_filter.real_last_impulsion) + "," + str(
                proportioned_filter.type) + "," + str(
                proportioned_filter.resolution_frequency) + "," + str(
                proportioned_filter.real_start_frequency) + "," + str(
                proportioned_filter.real_end_frequency) + "," + str(
                proportioned_filter.real_cut_off) + "," + str(
                proportioned_filter.resolution_db) + "," + str(
                proportioned_filter.dephasing) + "," + str(
                proportioned_filter.priority) + "," + str(
                proportioned_filter.attached) + "," + str(
                proportioned_filter.relativeOrAbsolute) + "," + str(parent_cut_off) + "," +str(proportioned_filter.parent)+ "," + str(proportioned_filter.attached_to_parent) +")"

    def __add_frequency_range__(self,frequency1,frequency2):
        self.string_equation = self.string_equation + "*frequency_range" + "(" + str(frequency1) + "," + str(frequency2) + ")"

    def __add_periodicity__(self,frequency,pattern):
        self.string_equation = self.string_equation + "*periodicity" + "(" + str(frequency) + "," + str(pattern) + ")"

    def __build_equation__(self):
        for i in range(0,len(self.filter_fusion.transfer_functions)):
            if self.filter_fusion.transfer_functions[i].type == "passe bas":
                self.__add_low_pass_filter__(self.filter_fusion.transfer_functions[i].cutoff1)

            if self.filter_fusion.transfer_functions[i].type == "passe haut":
                self.__add_high_pass_filter__(self.filter_fusion.transfer_functions[i].cutoff1)

            if (len(self.filter_fusion.transfer_functions) - 1 == i):
                self.__add_frequency_range__(self.filter_fusion.transfer_functions[i].frequency_min, "infinity")
            else:
                self.__add_frequency_range__(self.filter_fusion.transfer_functions[i].frequency_min, self.filter_fusion.transfer_functions[i].frequency_max)

            if self.filter_fusion.transfer_functions[i].proportioned_filter != None :
                self.__build_proportionned_equation__(self.filter_fusion.transfer_functions[i].proportioned_filter,self.filter_fusion.transfer_functions[i].cutoff1)

    def __build_proportionned_equation__(self, proportionned_filters,parent_cut_off):
        for i in range(0,len(proportionned_filters)):
            if proportionned_filters[i].type == "passe bas routed":
                self.__add_routed_low_pass_filter__(proportionned_filters[i],parent_cut_off)
            if proportionned_filters[i].type == "passe haut routed":
                self.__add_routed_high_pass_filter__(proportionned_filters[i],parent_cut_off)

            self.__add_frequency_range__(proportionned_filters[i].dephased_first_frequency,
                                         proportionned_filters[i].dephased_last_frequency)
            self.__add_periodicity__(proportionned_filters[i].periodic_frequency,proportionned_filters[i].pattern)

            if proportionned_filters[i].proportioned_filters != None:
                self.__build_proportionned_equation__(proportionned_filters[i].proportioned_filters,proportionned_filters[i].real_cut_off)
