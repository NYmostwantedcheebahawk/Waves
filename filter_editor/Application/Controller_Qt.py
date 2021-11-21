import Waves.filter_editor.Application.Event as events
import Waves.filter_editor.Application.View as view

class controller_qt:
    """
    Control l'orchestration ainsi que les appelles de fonction de la vue nécessaires pour que celle-ci soit mis à jours
    """
    def __init__(self,model,controller):
        """
        :param model: -> pipeline > le pipeline du controlleur
        :param interface -> graphical_interface > l'interface graphique du controlleur
        :param controller -> controller > l'objet controller
        """
        self.model = model
        self.my_interface = view.graphical_interface()
        self.my_interface.dashboard_window.define()
        self.show_dashboard_window()
        self.events = events.events(controller, self.my_interface)
        self.define_connects()
        self.redefine_vue()


    def intialisation(self, model, data_index):
        """
        sert à initialiser les dernières informations nécessaires pour la vue
        :param model: -> pipeline > le pipeline du controlleur
        :param data_index: -> int > position de la transformation dans le pipeline
        """
        self.dataX = self.define_x_data(model,data_index)
        self.dataY = self.define_y_data(model,data_index)

    def define_connects(self):
        """
        :param model: -> pipeline > le pipeline du controlleur
        Définie toute les connection entre les objets qt et les événements
        """
        self.my_interface.dashboard_window.filter_fusion.triggered.connect(self.events.__add_filter_event__)
        self.my_interface.dashboard_window.routed_filter.triggered.connect(self.events.__add_routed_filter_event__)
        self.my_interface.dashboard_window.phase.triggered.connect(self.events.__switch_to_phase__)
        self.my_interface.dashboard_window.bode.triggered.connect(self.events.__switch_to_bode__)
        self.my_interface.dashboard_window.equation.triggered.connect(self.events.__compute_equation_event__)

    def define_x_data(self,model,data_index = -1):
        """
        :param model: -> pipeline > le pipeline du controlleur
        :param data_index: -> int > position de la transformation dans le pipeline
        :return: -> x
        sert à définir les données en x temporelle
        """
        x = model.data.transformations[data_index].state.freq
        return x

    def define_y_data(self,model,data_index = -1):
        """
        :param model: -> pipeline > le pipeline du controlleur
        :param data_index: -> int > position de la transformation dans le pipeline
        :return: -> y
        sert à définir les données en y temporelle
        """
        y =  model.data.transformations[data_index].state.impulsion
        return y

    def redefine_vue(self, data_index=-1):
        """
        Cette fonction orchestre toute les changement nécessaire pour mettre à jours la vue
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        """
        self.intialisation(self.model,data_index)
        self.redefine_graphic_window(self.my_interface.graphical_window)

    def redefine_graphic_window(self, window):
        """
        :param window: -> QWindow > la fenêtre que l'on veut modifier
        redéfinir le graphique du temps
        """
        window.set_curve(self.dataX, self.dataY)
        self.my_interface.show_graphic(window)


    def show_dashboard_window(self):
        """
        permet d'afficher le dashboard
        """
        self.my_interface.show_dashboard_window()

    def define_plot(self, dataX, dataY, window_type, name):
        window_type.set_curve(dataX,dataY,name)
        window_type.qwt_plot.replot()
        window_type.qwt_plot.show()
        self.my_interface.show_dashboard_filter_editing_window()

    def redefine_vue_equation(self,equation_decoder):
        """
        Cette fonction orchestre toute les changement nécessaire pour mettre à jours la vue
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        """
        dataX = []
        dataY = []
        for i in range(0,2000):
            dataX.append(i)
            if i == 700 or i == 400:
                print(i)
            dataY.append(equation_decoder.__get_impulsion__(i))
        self.my_interface.graphical_window_test_equation.set_curve(dataX,dataY)
        self.my_interface.show_graphic(self.my_interface.graphical_window_test_equation)
