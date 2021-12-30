import math
from Waves.filter_editor.utilities.filter_equations import *
class filter_fusion():

    def __init__(self,transfer_function):
        self.name = "transfer_function"
        self.transfer_functions = [transfer_function]

    def __insert_transfer_function__(self, transfer_function):
        self.transfer_functions.insert(-1,transfer_function)

    def __change_cutoff_1__(self, cutoff):
        for x in range(0,len(self.transfer_functions)):
            if self.transfer_functions[x].frequency_min <= cutoff and self.transfer_functions[x].frequency_max >= cutoff:
                self.transfer_functions[x].cutoff1 = cutoff

    def __change_cutoff_2__(self, cutoff):
        for x in range(0,len(self.transfer_functions)):
            if self.transfer_functions[x].frequency_min <= cutoff and self.transfer_functions[x].frequency_max >= cutoff:
                self.transfer_functions[x].cutoff2 = cutoff

