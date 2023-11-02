import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog, QVBoxLayout, QLineEdit, QPushButton, \
    QLabel, QWidget

import Client
import DataBase
import Serve
from Tools import generate_new_id
from sources.momotalk_ui import Ui_Form  # 导入生成的UI文件


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('MomoTalk - 在线聊天室')
        # 添加最近30条消息
        recent_messages = DataBase.get_recent_messages()
        for message in recent_messages:
            name, text = message.content.split(":", 1)
            Client.add_msg2list(Client.message_format2list(text, name, message.time, message.sender),
                                self.pub_msg_list)

        # 绑定所有的？按钮事件
        self.pub_btn_help.clicked.connect(self.help_btn_clicked)
        self.pri_btn_help.clicked.connect(self.help_btn_clicked)
        self.per_btn_help.clicked.connect(self.help_btn_clicked)

        # 绑定发送按钮事件
        self.pub_btn_send.clicked.connect(self.pub_btn_send_clicked)
        self.pri_btn_send.clicked.connect(self.pri_btn_send_clicked)
        self.per_btn_send.clicked.connect(self.per_btn_send_clicked)

        # 定时器用于更新时间
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_time)

        # 登录界面按钮
        self.ifo_btn_changeAC.clicked.connect(self.show_login_window)

        # 更换匿名按钮
        self.pri_btn_change.clicked.connect(self.change_pri_name)

        # 在登录账号之前，一系列按钮、编辑框都是不可用状态
        self.pub_btn_send.setEnabled(False)
        self.pri_btn_send.setEnabled(False)
        self.per_btn_send.setEnabled(False)
        self.pri_btn_change.setEnabled(False)
        self.per_btn_search.setEnabled(False)
        self.ifo_user_name.setEnabled(False)
        self.ifo_user_sex.setEnabled(False)
        self.ifo_user_date.setEnabled(False)
        self.ifo_user_mail.setEnabled(False)
        self.ifo_user_info.setEnabled(False)
        self.ifo_btn_changePW.setEnabled(False)
        self.ifo_btn_edit.setEnabled(False)

        # 绑定查询用户按钮
        self.per_btn_search.clicked.connect(self.per_btn_search_clicked)

        # 绑定修改密码按钮
        self.ifo_btn_changePW.clicked.connect(self.show_change_password_window)

        # 绑定编辑个人信息按钮
        self.ifo_btn_edit.clicked.connect(self.ifo_btn_edit_clicked)

    # 按下帮助按钮后跳转进帮助界面
    def help_btn_clicked(self):
        self.tabWidget.setCurrentIndex(4)

    # 公共聊天室发送按钮事件
    def pub_btn_send_clicked(self):
        text = self.pub_msg_input.toPlainText()
        self.pub_msg_input.setText('')
        if text != '':
            Client.send(Client.user.name + ':' + str(text), "ALL", '201')

    # 匿名聊天室发送按钮事件
    def pri_btn_send_clicked(self):
        text = self.pri_msg_input.toPlainText()
        self.pri_msg_input.setText('')
        if text != '':
            Client.send(self.pri_lable_name.text() + ':' + str(text), "ALL", '202')

    # 私人聊天室发送按钮事件
    def per_btn_send_clicked(self):
        text = self.per_msg_input.toPlainText()
        self.per_msg_input.setText('')
        if text != '':
            receiver_id = self.per_text_searchId.text()
            if DataBase.get_user_by_id(receiver_id) is not None:
                Client.send(Client.user.name + ':' + str(text), receiver_id, '203')
            else:
                self.show_dialog('您输入的用户id不存在')

    # 左下角的时间显示函数
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.pub_lable_time.setText(f"{current_time}")
        self.pri_lable_time.setText(f"{current_time}")
        self.per_lable_time.setText(f"{current_time}")
        self.ifo_lable_time.setText(f"{current_time}")

    # 登录界面
    def show_login_window(self):
        login_window = LoginWindow()
        result = login_window.exec_()  # 阻塞直到登录窗口关闭
        if result == QDialog.Accepted:
            # 成功登录后跟新资料
            self.client_init()
        else:
            print("登录窗口关闭")

    # 修改密码界面
    def show_change_password_window(self):
        change_window = ChangePasswordWindow()
        result = change_window.exec_()

        # 切换匿名

    def change_pri_name(self):
        name = random.choice(Serve.users_name)
        Serve.users_name.remove(name)
        Serve.users_name.append(self.pri_lable_name.text())
        self.pri_lable_name.setText(name)

    def show_dialog(self, msg):
        # 使用information信息框
        QMessageBox.information(self, "提示", msg, QMessageBox.Ok)

    # 登录客户端后要进行的初始化程序
    def client_init(self):
        # 启用功能
        self.pub_btn_send.setEnabled(True)
        self.pri_btn_send.setEnabled(True)
        self.per_btn_send.setEnabled(True)
        self.pri_btn_change.setEnabled(True)
        self.per_btn_search.setEnabled(True)
        self.ifo_btn_changePW.setEnabled(True)
        self.ifo_btn_edit.setEnabled(True)

        # 分配一个匿名
        pri_name = random.choice(Serve.users_name)
        Serve.users_name.remove(pri_name)
        self.pri_lable_name.setText(pri_name)

        # 更新用户资料
        self.ifo_user_id.setText(Client.user.id)
        self.ifo_user_name.setText(Client.user.name)
        self.ifo_user_sex.setCurrentText(Client.user.sex)
        self.ifo_user_date.setDate(QDate.fromString(Client.user.birthday, "yyyy-MM-dd"))
        self.ifo_user_mail.setText(Client.user.mail)
        self.ifo_user_info.setText(Client.user.info)

    def per_btn_search_clicked(self):
        user_ifo = DataBase.get_user_by_id(self.per_text_searchId.text())
        if user_ifo is not None:
            self.show_user_info(user_ifo)
        else:
            self.show_dialog('用户不存在')

    def show_user_info(self, user):
        message = (f"ID:     {user.id}\n昵称: {user.name}\n性别: {user.sex}\n"
                   f"生日: {user.birthday}\n邮箱: {user.mail}\n简介: {user.info}")
        self.show_dialog(message)

    # 关闭界面前执行的
    def closeEvent(self, event):
        Serve.users_name.append(self.pri_lable_name.text())

        event.accept()  # 关闭窗口

    def ifo_btn_edit_clicked(self):
        if self.ifo_btn_edit.text() == '编辑资料':
            self.ifo_btn_edit.setText('完成修改')

            self.ifo_user_name.setEnabled(True)
            self.ifo_user_sex.setEnabled(True)
            self.ifo_user_date.setEnabled(True)
            self.ifo_user_mail.setEnabled(True)
            self.ifo_user_info.setEnabled(True)

        else:
            self.ifo_btn_edit.setText('编辑资料')

            self.ifo_user_name.setEnabled(False)
            self.ifo_user_sex.setEnabled(False)
            self.ifo_user_date.setEnabled(False)
            self.ifo_user_mail.setEnabled(False)
            self.ifo_user_info.setEnabled(False)

            id = self.ifo_user_id.text()
            name = self.ifo_user_name.text()
            sex = str(self.ifo_user_sex.currentText())
            date = self.ifo_user_date.date().toString("yyyy-MM-dd")
            mail = self.ifo_user_mail.text()
            info = self.ifo_user_info.toPlainText()
            DataBase.update_user_info(id, name, sex, date, mail, info)

            self.show_dialog('修改成功！')


# 登录窗口
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录")
        self.setModal(True)
        self.resize(300, 150)

        layout = QVBoxLayout()

        self.username_label = QLineEdit(self)
        self.username_label.setPlaceholderText("请输入id")
        layout.addWidget(self.username_label)

        self.password_label = QLineEdit(self)
        self.password_label.setPlaceholderText("请输入密码")
        # 将密码框设置为密文
        self.password_label.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)

        login_button = QPushButton("登录")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        creat_ac_button = QPushButton("注册")
        creat_ac_button.clicked.connect(self.show_regist_window)
        layout.addWidget(creat_ac_button)

        self.setLayout(layout)

    # 添加逻辑验证部分
    def login(self):
        # 获取用户输入的信息
        id = self.username_label.text()
        password = self.password_label.text()

        # 向服务器发起检验请求
        if Client.is_valid_account(id, password):
            Client.user = DataBase.get_user_by_id(id)
            Serve.users.append(id)
            self.accept()
        else:
            QMessageBox.information(self, "错误", "账号登录失败！请检查账号或密码是否正确输入")

    # 用户注册界面
    def show_regist_window(self):
        regist_window = RegistrationWindow()
        result = regist_window.exec_()  # 阻塞直到登录窗口关闭


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

    # 注册逻辑
    def register(self):
        # 在这里添加用户注册逻辑，获取各个字段的值
        id = self.id_label.text()
        password = self.password_label.text()
        name = self.name_label.text()

        if name != '' and password != '' and ('>' not in password + name):
            # 向服务器发送添加账号数据的请求
            content = id + '>' + name + '>' + password
            DataBase.add_user(id, password, name, '保密', '1997-12-31', '', '这个人很懒，还什么都没有写哦')
            # 注册成功关闭窗口
            self.accept()
            # 显示注册成功消息框
            QMessageBox.information(self, "注册成功", "注册成功！")
        else:
            QMessageBox.information(self, "错误", "存在非法字符！")


# 修改密码窗口
class ChangePasswordWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("修改密码")
        self.setModal(True)
        self.resize(300, 150)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.user_id_label = QLineEdit(self)
        self.user_id_label.setPlaceholderText("请输入您的id")
        layout.addWidget(self.user_id_label)

        self.old_password_label = QLineEdit(self)
        self.old_password_label.setPlaceholderText("请输入原密码")
        self.old_password_label.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.old_password_label)

        self.new_password_label = QLineEdit(self)
        self.new_password_label.setPlaceholderText("请输入新密码")
        # 将密码框设置为密文
        self.new_password_label.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_label)

        change_button = QPushButton("确定")
        change_button.clicked.connect(self.change)
        layout.addWidget(change_button)

    def change(self):
        # 获取用户输入的信息
        old_password = self.old_password_label.text()
        new_password = self.new_password_label.text()
        sys_password = DataBase.get_password_by_id(self.user_id_label.text())

        # 判断是否合法并写入
        if ">" in new_password:
            QMessageBox.information(self, "错误", "新密码含非法字符")
        elif sys_password is None:
            QMessageBox.information(self, "错误", "用户名输入错误")
        elif sys_password != old_password:
            QMessageBox.information(self, "错误", "原密码输入错误")
        else:
            DataBase.update_user_password(self.user_id_label.text(), new_password)
            QMessageBox.information(self, "提示", "修改成功")
            self.accept()
