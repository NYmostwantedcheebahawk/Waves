import Waves.filter_editor.Application.Model as models
from Waves.filter_editor.Application.Controller_Qt import controller_qt
from Waves.filter_editor.editors.bode_plot_editor import bode_plot_editor
from Waves.filter_editor.editors.plot_editor import plot_editor
from Waves.filter_editor.utilities.filter_fusion import filter_fusion
from Waves.filter_editor.utilities.transfert_function import transfer_function

class Controller():
    """
    class qui permet d'ajouter les nouvelles transformation dans le pipeline en plus de trigger le controlleur d'affichage
    """
    def __init__(self,view_type):
        """
        Init: reçois les argument sys.argv pour contruire un Qt application
        data_file: fichier contenant les donnees
        """
        self.transfer_function = transfer_function(200, None, 1, 1,1, None, None, None, "passe bas", 0, None,1000,None,None,None)
        self.filter_fusion = filter_fusion(self.transfer_function)
        self.plot_editor = plot_editor("Bode",0, 1000, 1, self.filter_fusion)
        self.model = models.Model(self.plot_editor)
        self.model.data.transformations[-1].__calculate_transfer_function__()

        if(view_type == "controller_qt"):
            self.controller_qt = controller_qt(self.model,self)

    def add_manual_modification(self, first, last, attenuation):
        """
        :param first: -> la première sélection de donnée dans la structure
        :param last: -> la deuxième sélection de donnée dans la structure
        """
        self.model.data.transformations[-1].__insert_manual_modification__(first, last, attenuation)
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()

    def add_filter(self,cutoff1, cutoff2, order, resolution, resolutiondb, frequency_handicap, impulsion_handicap, type, frequency_min, frequency_middle ,frequency_max, impulsion_first, impulsion_middle, impulsion_last,manual_modification = None):
        transfer_function_to_add = transfer_function(cutoff1,cutoff2, order, resolution,resolutiondb, frequency_handicap,
                                                     impulsion_handicap, None, type,frequency_min, frequency_middle,
                                                     frequency_max, impulsion_first, impulsion_middle, impulsion_last,manual_modification)
        self.model.data.transformations[-1].__insert_transfer_function__(transfer_function_to_add)
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()

    def add_routed_filter(self, proportion_filter):
        self.model.data.transformations[-1].state.filter_fusion.transfer_functions[-1].__insert_proportioned_filter__(
            self.model.data.transformations[-1].__calculate_routed_filter__(proportion_filter, self.model.data.transformations[-1].state.filter_fusion.transfer_functions))
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()

    def switch_state(self,state):
        self.model.data.transformations[-1].__change_state__(state)
        self.model.data.transformations[-1].__calculate_transfer_function__()
        self.controller_qt.redefine_vue()
