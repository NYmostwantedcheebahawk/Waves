import sys

from PyQt5.Qt import (QWidget, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QSlider, QApplication, QPushButton, QLineEdit, QAction


from qwt import (QwtPlot, QwtPlotCurve, QwtText, QwtLogScaleEngine)
from scipy import signal


def instanciate_qt_application():
    """
    Instanciation d'une QApplication
    """
    return QApplication(sys.argv)


class graphical_interface():
    """
    Contient des attributs qui contient le différente QWindow
    Contient les fonction d'affichage
    """

    def __init__(self):
        """
        Instantiation des 4 différentes types de fenêtres
        """
        self.graphical_window = wrapper_qwt(graphical_window())
        self.graphical_window_test_equation = wrapper_qwt(graphical_window())
        self.dashboard_window = dashboard()

    def show_graphic(self,window):
        """
        affichage d'un graphique
        """
        window.state.qwt_plot.resize(600, 300)
        window.state.qwt_plot.replot()
        window.state.qwt_plot.show()

    def show_dashboard_window(self):
        """
        affichage du dashboard
        """
        self.dashboard_window.layout_.addLayout(self.dashboard_window.layout_text)
        self.dashboard_window.layout_.addLayout(self.dashboard_window.layout_text2)
        self.dashboard_window.layout_.addLayout(self.dashboard_window.layout_text3)
        self.dashboard_window.widget.setLayout(self.dashboard_window.layout_)
        self.dashboard_window.setCentralWidget(self.dashboard_window.widget)
        self.dashboard_window.show()


class pipeline_content(QWidget):
    """
    Defini les outils Qt utiliser dans la pipeline
    """
    def __init__(self):
        super(pipeline_content, self).__init__()
        self.pipeline_index = None
        self.pipeline_slider =  QSlider()

class dashboard(QMainWindow):
   """
   le dashboard contient toute les QObjects nécessaires au fonctionnement des transformations
   """
   def __init__(self):

       super(dashboard, self).__init__()

       # instantiation du layout
       self.layout_text = QHBoxLayout()
       self.layout_text2 = QHBoxLayout()
       self.layout_text3 = QHBoxLayout()
       self.layout_ = QVBoxLayout()

       # instanciation du widget
       self.widget = dashboard_content()

       #instanciation du menu bar
       self.bar = self.menuBar()

       #instanciation des actions dans un menu
       self.file = self.bar.addMenu("File")
       self.export_wav = QAction("export wav", self)
       self.file.addAction(self.export_wav)

       # instanciation des actions dans un menu
       self.actions = self.bar.addMenu("Actions")
       self.cutoff1 = QAction("Cutoff1", self)
       self.cutoff2 = QAction("Cutoff2", self)
       self.filter_fusion = QAction("add filter", self)
       self.routed_filter = QAction("add routed filter", self)
       self.order = QAction("order", self)
       self.phase = QAction("changeToPhase",self)
       self.bode = QAction("changeToBode",self)
       self.equation = QAction("compute_equation",self)
       self.actions.addAction(self.cutoff1)
       self.actions.addAction(self.cutoff2)
       self.actions.addAction(self.filter_fusion)
       self.actions.addAction(self.routed_filter)
       self.actions.addAction(self.order)
       self.actions.addAction(self.phase)
       self.actions.addAction(self.bode)
       self.actions.addAction(self.equation)

   def define(self):
       """
       setting up the layout
       """
       self.layout_text.addWidget(self.widget.first_label)
       self.layout_text.addWidget(self.widget.first)
       self.layout_text.addWidget(self.widget.middle_label)
       self.layout_text.addWidget(self.widget.middle)
       self.layout_text.addWidget(self.widget.last_label)
       self.layout_text.addWidget(self.widget.last)
       self.layout_text.addWidget(self.widget.cut_off_label)
       self.layout_text.addWidget(self.widget.cut_off)
       self.layout_text.addWidget(self.widget.cut_off_label2)
       self.layout_text.addWidget(self.widget.cut_off2)
       self.layout_text.addWidget(self.widget.order_label)
       self.layout_text.addWidget(self.widget.order)
       self.layout_text2.addWidget(self.widget.resolution_label)
       self.layout_text2.addWidget(self.widget.resolution)
       self.layout_text2.addWidget(self.widget.type_label)
       self.layout_text2.addWidget(self.widget.type)

       self.layout_text3.addWidget(self.widget.proportioned)

       self.layout_text3.addWidget(self.widget.proportioned_impulsion_label_first)
       self.layout_text3.addWidget(self.widget.proportioned_impulsion_first)

       self.layout_text3.addWidget(self.widget.proportioned_impulsion_label_last)
       self.layout_text3.addWidget(self.widget.proportioned_impulsion_last)

       self.layout_text3.addWidget(self.widget.real_first_impulsion_label)
       self.layout_text3.addWidget(self.widget.real_first_impulsion)

       self.layout_text3.addWidget(self.widget.real_last_impulsion_label)
       self.layout_text3.addWidget(self.widget.real_last_impulsion)

       self.layout_text3.addWidget(self.widget.routed_filter_type_label)
       self.layout_text3.addWidget(self.widget.routed_filter_type)

       self.layout_text3.addWidget(self.widget.dephased_first_frequency_label)
       self.layout_text3.addWidget(self.widget.dephased_first_frequency)

       self.layout_text3.addWidget(self.widget.dephased_last_frequency_label)
       self.layout_text3.addWidget(self.widget.dephased_last_frequency)

       self.layout_text3.addWidget(self.widget.real_cut_off_label)
       self.layout_text3.addWidget(self.widget.real_cut_off)

       self.layout_text3.addWidget(self.widget.periodic_frequency_label)
       self.layout_text3.addWidget(self.widget.periodic_frequency)

       self.layout_text3.addWidget(self.widget.attached_label)
       self.layout_text3.addWidget(self.widget.attached)

       self.layout_text3.addWidget(self.widget.relative_or_absolute_label)
       self.layout_text3.addWidget(self.widget.relative_or_absolute)

       self.layout_text3.addWidget(self.widget.pattern_label)
       self.layout_text3.addWidget(self.widget.pattern)

class dashboard_content(QWidget):
    """
    Defini les outils Qt utiliser dans la pipeline
    """
    def __init__(self):
        super(dashboard_content, self).__init__()

        self.first_label = QLabel("First:")
        self.first = QLineEdit()
        self.middle_label = QLabel("Middle:")
        self.middle = QLineEdit();
        self.last_label = QLabel("Last:")
        self.last = QLineEdit()
        self.cut_off_label = QLabel("cut_off(1):")
        self.cut_off = QLineEdit()
        self.cut_off_label2 = QLabel("cut_off(2):")
        self.cut_off2 = QLineEdit()
        self.attenuation_num_taps = QLineEdit()
        self.order_label = QLabel("Order")
        self.order = QLineEdit()
        self.resolution_label = QLabel("resolution")
        self.resolution = QLineEdit()
        self.type_label = QLabel("type")
        self.type = QLineEdit()

        self.proportioned = QLabel("proportioned:")
        self.proportioned_impulsion_label_first = QLabel("proportioned first impulsion:")
        self.proportioned_impulsion_first = QLineEdit()

        self.proportioned_impulsion_label_last = QLabel("proportioned last impulsion:")
        self.proportioned_impulsion_last = QLineEdit()

        self.real_first_impulsion_label = QLabel("real first impulsion")
        self.real_first_impulsion = QLineEdit()

        self.real_last_impulsion_label = QLabel("real last impulsion:")
        self.real_last_impulsion = QLineEdit()

        self.routed_filter_type_label = QLabel("routed filter type:")
        self.routed_filter_type = QLineEdit()

        self.dephased_first_frequency_label = QLabel("dephased first frequency:")
        self.dephased_first_frequency = QLineEdit()

        self.dephased_last_frequency_label = QLabel("dephased last frequency:")
        self.dephased_last_frequency = QLineEdit()

        self.real_cut_off_label = QLabel("real_cut_off:")
        self.real_cut_off = QLineEdit()

        self.attached_label = QLabel("attached:")
        self.attached = QLineEdit()

        self.relative_or_absolute_label = QLabel("relativeOrAbsolute:")
        self.relative_or_absolute = QLineEdit()

        self.periodic_frequency_label = QLabel("periodic_frequency:")
        self.periodic_frequency = QLineEdit()

        self.pattern_label = QLabel("pattern:")
        self.pattern = QLineEdit()

class plot_state(QMainWindow):
    """
    Classe qui definit le minimum dans un état d'un graphique
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self):
        super(plot_state, self).__init__()
        self.qwt_plot = QwtPlot

    def set_curve(self,x,y):
        """
        :param x: -> float[] > valeurs représentant l'axe des x
        :param y: -> float[] > valeurs représentant l'axe des y
        :param name: -> string > nom de la courbe
        """
        self.curve.setData(x, y)
        self.curve.attach(self.qwt_plot)

class graphical_window(plot_state):
    """
    sous cette état le graphique affiche une courbe en temporelle
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self):
        super(graphical_window, self).__init__()
        self.name = ""
        self.curve = QwtPlotCurve(self.name)
        self.qwt_plot = QwtPlot(self.name)

class wrapper_qwt():
    """
    classe ajoutant des fonctionnalite a un qwtPlot
    """
    def __init__(self, state):
        super(wrapper_qwt, self).__init__()
        self.state = state


    def set_curve(self,x,y):
        """
        appelle la bonne definition pour definir la courbe selon l'etat
        """
        return self.state.set_curve(x,y)
