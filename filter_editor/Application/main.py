import sys
import Waves.filter_editor.Application.Controller as cont
import os
import Waves.filter_editor.Application.View as view

# Lance le programme à son emplacement
app = view.instanciate_qt_application()
program_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(program_folder)

filename = "/home/cheebahawkdesktop/Documents/test_files/aircraft_takeoff.csv"
control = cont.Controller("controller_qt")

sys.exit(app.exec_())