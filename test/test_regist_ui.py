import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QDialog, QLabel

from Tools import generate_new_id


class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户注册")
        self.setModal(True)
        self.resize(400, 250)

        layout = QVBoxLayout()

        self.ifo_label = QLabel(self)
        self.ifo_label.setText('您分配的账号为：')
        layout.addWidget(self.ifo_label)

        self.id_label = QLabel(self)
        self.id_label.setText(generate_new_id())
        layout.addWidget(self.id_label)

        self.name_label = QLineEdit(self)
        self.name_label.setPlaceholderText("姓名")
        layout.addWidget(self.name_label)

        self.password_label = QLineEdit(self)
        self.password_label.setPlaceholderText("密码")
        self.password_label.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)

        register_button = QPushButton("注册")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        self.setLayout(layout)

    # 注册逻辑（未完成）
    def register(self):
        # 在这里添加用户注册逻辑，获取各个字段的值
        id = self.id_label.text()
        password = self.password_label.text()
        name = self.name_label.text()
        print(id)
        print(password)
        print(name)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('用户注册界面')

        register_button = QPushButton('注册')
        register_button.clicked.connect(self.show_registration_window)

        layout = QVBoxLayout()
        layout.addWidget(register_button)
        self.setLayout(layout)

    def show_registration_window(self):
        registration_window = RegistrationWindow()
        result = registration_window.exec_()  # 阻塞直到注册窗口关闭
        if result == QDialog.Accepted:
            print("注册窗口关闭")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
