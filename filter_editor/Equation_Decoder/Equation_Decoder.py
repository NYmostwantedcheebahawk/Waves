from Waves.filter_editor.Equation_Decoder.proportioned_filter_equation import proportioned_filter_equation
from Waves.filter_editor.Equation_Decoder.frequency_range import frequency_range
from Waves.filter_editor.Equation_Decoder.transfert_function_equation import tranfert_function_equation
class Equation_Decoder():
    def __init__(self,equation):
        self.equation_string = equation
        self.filters = []
        self.frequency = []
        self.current_activated_filters = []
        self.current_priority = 0
        self.current_index = 0
    def __create_passive_filter__(self,cut_off,type):
        return tranfert_function_equation(cut_off,type)
    def __create_proportionned_filter__(self,dephased_first_frequency,dephased_last_frequency,proportioned_impulsion_first,proportioned_impulsion_last,real_first_impulsion,real_last_impulsion,routed_filter,resolution_frequency,real_start_frequency,real_end_frequency,real_cut_off,resolution_db, dephasing ,priority,attached,relativeOrAbsolute,parent_cut_off):
        return proportioned_filter_equation(dephased_first_frequency,dephased_last_frequency,proportioned_impulsion_first,proportioned_impulsion_last,real_first_impulsion,real_last_impulsion,routed_filter,resolution_frequency,real_start_frequency,real_end_frequency,real_cut_off,resolution_db, dephasing ,priority,attached,relativeOrAbsolute,parent_cut_off)
    def __update__(self,filter,frequency):
        if filter.__get_last_frequency__() == "check_frequency":
            pass
        else:
            if filter.__get_last_frequency__() <= frequency :
                self.frequency[self.current_index].__update_frequency_range__()
                filter.__update__(self.frequency[self.current_index].frequency1, self.frequency[self.current_index].frequency2)
    def __decode_equation__(self):
        array_different_filter = str(self.equation_string.string_equation).split("+")
        for i in range(0,len(array_different_filter)):
            array_element_per_filter = array_different_filter[i].split("*")
            for e in range(0,len(array_element_per_filter)):
               if "filter" in array_element_per_filter[e] and "routed" not in array_element_per_filter[e]:
                   if "low" in array_element_per_filter[e]:
                        position1 = array_element_per_filter[e].find("(")
                        position2 = array_element_per_filter[e].find(")")
                        self.filters.append(self.__create_passive_filter__(array_element_per_filter[e][position1+1 : position2],"lower_pass"))
                   if "high" in array_element_per_filter[e]:
                       position1 = array_element_per_filter[e].find("(")
                       position2 = array_element_per_filter[e].find(")")
                       self.filters.append(self.__create_passive_filter__(array_element_per_filter[e][position1 + 1: position2],"high_pass"))
               if "routed" in array_element_per_filter[e]:
                   array_routed_filter_parameter = array_element_per_filter[e].split(",")
                   position1 = array_routed_filter_parameter[0].find("(") + 1
                   parameter1 =array_routed_filter_parameter[0] [position1: len(array_routed_filter_parameter[0])]
                   index1 = len(array_routed_filter_parameter) -1
                   parameter2 = array_routed_filter_parameter[index1][0 :len(array_routed_filter_parameter[index1])-1]
                   self.filters.append(self.__create_proportionned_filter__(parameter1,array_routed_filter_parameter[1],array_routed_filter_parameter[2],array_routed_filter_parameter[3],array_routed_filter_parameter[4],array_routed_filter_parameter[5],array_routed_filter_parameter[6],array_routed_filter_parameter[7],array_routed_filter_parameter[8],array_routed_filter_parameter[9],array_routed_filter_parameter[10],array_routed_filter_parameter[11],array_routed_filter_parameter[12],array_routed_filter_parameter[13],array_routed_filter_parameter[14],array_routed_filter_parameter[15],parameter2))

               if "frequency_range" in array_element_per_filter[e]:
                   position1 = array_element_per_filter[e].find("(")
                   position2 = array_element_per_filter[e].find(",")
                   position3 = array_element_per_filter[e].find(")")
                   self.frequency.append(frequency_range(array_element_per_filter[e][position1+1:position2],array_element_per_filter[e][position2+1:position3]))

               if "periodicity" in array_element_per_filter[e]:
                   position1 = array_element_per_filter[e].find("(")
                   position2 = array_element_per_filter[e].find(",")
                   position3 = array_element_per_filter[e].find(")")
                   self.frequency[i].__add_periodicity__(array_element_per_filter[e][position1+1:position2],array_element_per_filter[e][position2+1:position3])


    def __get_impulsion__(self,frequency):
        self.__update__(self.filters[self.current_index],frequency)
        self.current_priority = 0
        self.current_index = 0
        for i in range(0,len(self.frequency)):
            if self.frequency[i].__within_frequency__(frequency) :
                if self.current_priority < int(self.filters[i].priority):
                    self.current_index = i

        return self.filters[self.current_index].__get_impulsion__(frequency)



