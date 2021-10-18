from Waves.filter_editor.utilities.proportioned_filter import proportioned_filter


class events:
    """
    class permettant d'appeler des evenements pour créer des transformation
    """
    def __init__(self, controller, my_interface):
        """
        :param controller: -> controller > la référence au controller
        """
        self.controller = controller
        self.my_interface = my_interface

    def __add_manual_modification_event__(self):
        """
        permet de prendre une fourchette de donnée modifier et de la réintégrer dans l'ensemble des données
        """
        first = 0
        last = 0
        attenuation = 0
        if self.my_interface.dashboard_window.widget.cut_off.text() != '':
            first = int(self.my_interface.dashboard_window.widget.cut_off.text())
        if self.my_interface.dashboard_window.widget.cut_off2.text() != '':
            last = int(self.my_interface.dashboard_window.widget.cut_off2.text())
        if self.my_interface.dashboard_window.widget.attenuation_num_taps.text() != '':
            attenuation = int(self.my_interface.dashboard_window.widget.attenuation_num_taps.text())
        self.controller.add_manual_modification(first, last, attenuation)

    def __add_filter_event__(self):
        first = 0
        middle = 0
        last = 0
        cut_off1 = 0
        cut_off2 = 0
        order = 1
        handicap_frequency = 0
        handicap_impulsion = 0
        resolution = 1
        resolutiondb = 1
        type = "passe bas"
        first_impulsion = 0;
        middle_impulsion = 0;
        last_impulsion = 0;
        if self.my_interface.dashboard_window.widget.first.text() != '':
            first = int(self.my_interface.dashboard_window.widget.first.text())
        if self.my_interface.dashboard_window.widget.last.text() != '':
            last = int(self.my_interface.dashboard_window.widget.last.text())
        if self.my_interface.dashboard_window.widget.cut_off.text() != '':
            cut_off1 = int(self.my_interface.dashboard_window.widget.cut_off.text())
        if self.my_interface.dashboard_window.widget.cut_off2.text() != '':
            cut_off2 = int(self.my_interface.dashboard_window.widget.cut_off2.text())
        if self.my_interface.dashboard_window.widget.order.text() != '':
            order = int(self.my_interface.dashboard_window.widget.order.text())
        if self.my_interface.dashboard_window.widget.handicap_frequency.text() != '':
            handicap_frequency = int(self.my_interface.dashboard_window.widget.handicap_frequency.text())
        if self.my_interface.dashboard_window.widget.handicap_impulsion.text() != '':
            handicap_impulsion = int(self.my_interface.dashboard_window.widget.handicap_impulsion.text())
        if self.my_interface.dashboard_window.widget.resolution.text() != '':
            resolution = int(self.my_interface.dashboard_window.widget.resolution.text())
        if self.my_interface.dashboard_window.widget.type.text() != '':
            type = self.my_interface.dashboard_window.widget.type.text()
        self.controller.add_filter(cut_off1, None, order, resolution,resolutiondb ,handicap_frequency, handicap_impulsion, type, first, middle,last,first_impulsion,middle_impulsion,last_impulsion)

    def __add_routed_filter_event__(self):

        proportioned_impulsion_first = 0;
        proportioned_impulsion_last = 0;
        real_first_impulsion = 0;
        real_last_impulsion = 0;
        routed_filter_type = '';
        dephased_first_frequency = -1;
        dephased_last_frequency = -1;
        real_cut_off = 0

        if self.my_interface.dashboard_window.widget.proportioned_impulsion_first.text() != '':
            proportioned_impulsion_first = self.my_interface.dashboard_window.widget.proportioned_impulsion_first.text()
        if self.my_interface.dashboard_window.widget.proportioned_impulsion_last.text() != '':
            proportioned_impulsion_last = self.my_interface.dashboard_window.widget.proportioned_impulsion_last.text()
        if self.my_interface.dashboard_window.widget.real_first_impulsion.text() != '':
            real_first_impulsion = self.my_interface.dashboard_window.widget.real_first_impulsion.text()
        if self.my_interface.dashboard_window.widget.real_last_impulsion.text() != '':
            real_last_impulsion = self.my_interface.dashboard_window.widget.real_last_impulsion.text()
        if self.my_interface.dashboard_window.widget.routed_filter_type.text() == "passe bas routed":
            routed_filter_type = "passe bas routed"
        if self.my_interface.dashboard_window.widget.routed_filter_type.text() == "passe haut routed":
            routed_filter_type = "passe haut routed"
        if self.my_interface.dashboard_window.widget.dephased_first_frequency.text() != '':
            dephased_first_frequency = self.my_interface.dashboard_window.widget.dephased_first_frequency.text()
        if self.my_interface.dashboard_window.widget.dephased_last_frequency.text() != '':
            dephased_last_frequency = self.my_interface.dashboard_window.widget.dephased_last_frequency.text()
        if self.my_interface.dashboard_window.widget.real_cut_off.text() != '':
            real_cut_off = self.my_interface.dashboard_window.widget.real_cut_off.text()

        self.proportioned_filter = proportioned_filter(float(proportioned_impulsion_first), float(proportioned_impulsion_last), float(real_first_impulsion), float(real_last_impulsion), routed_filter_type, float(dephased_first_frequency), float(dephased_last_frequency),float(real_cut_off))
        self.controller.add_routed_filter(self.proportioned_filter)

    def __switch_to_phase__(self):
        self.controller.switch_state("Phase")

    def __switch_to_bode__(self):
        self.controller.switch_state("Bode")









