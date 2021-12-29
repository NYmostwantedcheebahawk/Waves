import Waves.filter_editor.Application.Model as models
from Waves.filter_editor.Application.Controller_Qt import controller_qt
from Waves.filter_editor.editors.bode_plot_editor import bode_plot_editor
from Waves.filter_editor.editors.plot_editor import plot_editor
from Waves.filter_editor.utilities.filter_equations import filter_equations
from Waves.filter_editor.utilities.filter_fusion import filter_fusion
from Waves.filter_editor.utilities.transfert_function import transfer_function
from Waves.filter_editor.utilities.Equation_Maker import Equation_Maker
from Waves.filter_editor.Equation_Decoder.Equation_Decoder import Equation_Decoder

class Controller():
    """
    class qui permet d'ajouter les nouvelles transformation dans le pipeline en plus de trigger le controlleur d'affichage
    """
    def __init__(self,view_type):
        """
        Init: reçois les argument sys.argv pour contruire un Qt application
        data_file: fichier contenant les donnees
        """
        self.transfer_function = transfer_function(200, None, 1, 1,1,"passe bas", 0, None,1000,None,None,None)
        self.filter_fusion = filter_fusion(self.transfer_function)
        self.plot_editor = plot_editor("Bode",0, 1000, 1, self.filter_fusion)
        self.model = models.Model(self.plot_editor)
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.priority = 0

        if(view_type == "controller_qt"):
            self.controller_qt = controller_qt(self.model,self)


    def add_filter(self,cutoff1, cutoff2, order, resolution, resolutiondb, type, frequency_min, frequency_middle ,frequency_max, impulsion_first, impulsion_middle, impulsion_last):
        transfer_function_to_add = transfer_function(cutoff1, cutoff2, order, resolution, resolutiondb, None, type, frequency_min, frequency_middle, frequency_max, impulsion_first, impulsion_middle, impulsion_last)
        self.model.data.transformations[-1].__insert_transfer_function__(transfer_function_to_add)
        ##here
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()

    def add_routed_filter(self, proportion_filter):
        self.priority  = self.priority +1
        filter = filter_equations.find_filter(filter_equations, proportion_filter.real_first_impulsion,
                                     proportion_filter.real_first_impulsion,
                                     proportion_filter.dephased_first_frequency,
                                     proportion_filter.dephased_last_frequency, self.model.data.transformations[-1].state.filter_fusion.transfer_functions)
        new_proportion_filter = self.model.data.transformations[-1].__calculate_routed_filter__(proportion_filter, self.model.data.transformations[-1].state.filter_fusion.transfer_functions)
        new_proportion_filter.priority = self.priority
        filter.__insert_proportioned_filter__(new_proportion_filter)
        i1 = 0
        if "routed" not in filter.type:
            if "bas" in filter.type:
                i1 = filter_equations.log_time_20(filter_equations,filter_equations.lower_pass_bode(filter_equations,proportion_filter.dephased_last_frequency,filter.cutoff1))
            elif "haut" in filter.type:
                i1 = filter_equations.log_time_20(filter_equations,filter_equations.high_pass_bode(filter_equations,proportion_filter.dephased_last_frequency,filter.cutoff1))
        else:
            i1 = filter.__get_impulsion__(proportion_filter.dephased_last_frequency)

        proportion_filter.attached_to_parent = (proportion_filter.real_last_impulsion == i1)
        ##here
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()

    def switch_state(self,state):
        ##here
        self.model.data.transformations[-1].__change_state__(state)
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()

    def __get_equation_plot__(self):
        equation = Equation_Maker(self.filter_fusion)
        equation.__build_equation__()
        plot = Equation_Decoder(equation)
        plot.__decode_equation__()
        self.controller_qt.redefine_vue_equation(plot)
