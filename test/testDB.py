import importlib
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import DataBase
from GUI import MyMainForm


def show_page():
    app = QApplication(sys.argv)
    window = MyMainForm()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    DataBase.add_message("d","s","S","s","s")
