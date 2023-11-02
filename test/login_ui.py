import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

from GUI import CustomDialog


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录界面')
        self.setGeometry(100, 100, 300, 150)

        # 创建标签和文本框
        self.username_label = QLabel('用户名:')
        self.username_textbox = QLineEdit(self)
        self.password_label = QLabel('密码:')
        self.password_textbox = QLineEdit(self)
        self.password_textbox.setEchoMode(QLineEdit.Password)

        # 创建登录按钮
        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.login)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_textbox)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_textbox.text()
        password = self.password_textbox.text()
        # 在这里添加登录验证逻辑，例如检查用户名和密码是否匹配
        # 这里只是一个示例，你需要根据实际情况进行验证



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
