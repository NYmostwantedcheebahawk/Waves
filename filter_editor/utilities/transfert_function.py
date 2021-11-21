from Waves.filter_editor.utilities.filter_equations import *
class transfer_function():

    def __init__(self, cutoff1,cutoff2, order, resolution, resolutiondb, type, frequency_min, frequency_middle, frequency_max, impulsion_first, impulsion_middle, impulsion_last,proportioned_filter =None):
        self.name = "transfer_function"
        self.cutoff1 = cutoff1
        self.cutoff2 = cutoff2
        self.order = order
        self.frequency_min = frequency_min
        self.frequency_middle = frequency_middle
        self.routed_min_frequency =0
        self.routed_max_frequency =0
        self.db_dephasing = 0
        self.frequency_max = frequency_max
        self.resolution = resolution
        self.resolution_db = resolutiondb
        self.type = type
        self.filter_equation = filter_equations()
        self.priority = 0
        if impulsion_first == None:
            self.impulsion_first = filter_equations.log_time_20(self,filter_equations.lower_pass_bode(self,frequency_min,cutoff1))
        else:
            self.impulsion_first = impulsion_first
        self.impulsion_middle = impulsion_middle
        if impulsion_last == None:
            self.impulsion_last = filter_equations.log_time_20(self,filter_equations.lower_pass_bode(self,frequency_max,cutoff1))
        else:
            self.impulsion_last = impulsion_last
        if (proportioned_filter != None):
            self.proportioned_filter = [proportioned_filter]
        else:
            self.proportioned_filter = None

    def __plug__(self, transfer_function):
        self.name = "transfer_function"
        self.cutoff1 = transfer_function.cutoff1
        self.cutoff2 = transfer_function.cutoff2
        self.order = transfer_function.order
        self.frequency_min = transfer_function.frequency_min
        self.frequency_middle = transfer_function.frequency_middle
        self.frequency_max = transfer_function.frequency_max
        self.resolution = transfer_function.resolution
        self.resolution_db = transfer_function.resolution_db
        self.type = transfer_function.type
        self.manual_modifications = transfer_function.manual_modifications
        self.impulsion_first = transfer_function.impulsion_first
        self.impulsion_middle = transfer_function.impulsion_middle
        self.impulsion_last = transfer_function.impulsion_last
        self.proportioned_filter = transfer_function.proportioned_filter

    def __define_routable_attributes__(self,routed_min_frequency,routed_max_frequency,db_dephasing):
        self.routed_min_frequency = routed_min_frequency
        self.routed_max_frequency = routed_max_frequency
        self.db_dephasing = db_dephasing

    def __modify_cutoff1__(self, cutoff1):
        self.cutoff1 = cutoff1

    def __modify_cutoff2__(self, cutoff2):
        self.cutoff2 = cutoff2

    def __modify_order___(self, order):
        self.order = order

    def __modify_frequency_min__(self, frequency_min):
        self.frequency_min = frequency_min

    def __modify_frequency_max__(self, frequency_max):
        self.frequency_max = frequency_max

    def __modify_resolution__(self, resolution):
        self.resolution = resolution

    def __modify_type__(self, type):
        self.type = type

    def __insert_proportioned_filter__(self, proportioned_filter):
        if(self.proportioned_filter == None):
            self.proportioned_filter = [proportioned_filter]
        else:
            self.proportioned_filter.insert(-1, proportioned_filter)