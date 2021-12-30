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

        self.plot_editor = plot_editor("Bode",0, 1000, 1)
        self.model = models.Model(self.plot_editor)
        self.model.data.transformations[-1].__calculate_transfer_function__()

        if(view_type == "controller_qt"):
            self.controller_qt = controller_qt(self.model,self)


    def add_filter(self,cutoff1, cutoff2, order, resolution, resolutiondb, type, frequency_min, frequency_middle ,frequency_max, impulsion_first, impulsion_middle, impulsion_last):
        self.model.data.transformations[-1].__add_filter__(cutoff1, cutoff2, order, resolution, resolutiondb, type, frequency_min, frequency_middle ,frequency_max, impulsion_first, impulsion_middle, impulsion_last)
        self.controller_qt.redefine_vue()

    def add_routed_filter(self, proportioned_impulsion_first, proportioned_impulsion_last, real_first_impulsion,
                 real_last_impulsion, routed_filter_type, dephased_first_frequency, dephased_last_frequency,
                 real_cut_off,periodic_frequency,relativeOrAbsolute,pattern,attached,proportioned_filter = None):

        self.model.data.transformations[-1].__add_routed_filter__(proportioned_impulsion_first, proportioned_impulsion_last, real_first_impulsion,real_last_impulsion, routed_filter_type, dephased_first_frequency, dephased_last_frequency,real_cut_off,periodic_frequency,relativeOrAbsolute,pattern,attached,proportioned_filter)
        self.controller_qt.redefine_vue()

    def switch_state(self,state):
        ##here
        self.model.data.transformations[-1].__change_state__(state)
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()

    def __get_equation_plot__(self):
        plot = Equation_Decoder(self.model.data.transformations[-1].__get_equation__())
        plot.__decode_equation__()
        self.controller_qt.redefine_vue_equation(plot)
