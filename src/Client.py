import datetime
import socket
import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication

import DataBase
import GUI
import Tools
from Message import Message
from User import User

# 服务器配置
HOST = '127.0.0.1'
PORT = 12345

# 登录状态
login_status = False

# 连接服务器
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# 当前用于
user = User('12345', '游客', '保密', '', '', '')
user_id = None


# 接收消息
def receive():
    while True:
        try:
            # 接收服务器发回的Message并做出响应
            message = client.recv(1024).decode('utf-8')
            msg = Tools.decode_json(message)
            print(msg)

            if msg.typecode == 'ERROR':
                window.show_dialog('出现未知错误，请检查')
            if msg.typecode == 'SUCCESS':
                global login_status
                login_status = True
            elif msg.typecode == '201':
                # 公共聊天室消息
                name, text = msg.content.split(":", 1)
                add_msg2list(message_format2list(text, name, msg.time, msg.sender), window.pub_msg_list)
            elif msg.typecode == '202':
                # 匿名聊天室消息
                name, text = msg.content.split(":", 1)
                add_msg2list(message_format2list(text, name, msg.time), window.pri_msg_list)
            elif msg.typecode == '203' and is_same(msg.receiver, msg.sender):
                # 私人聊天室消息
                name, text = msg.content.split(":", 1)
                add_msg2list(message_format2list(text, name, msg.time, msg.sender), window.per_msg_list)
            else:
                continue

        except:
            window.show_dialog('连接中断，请检查网络或服务器后重启软件')
            client.close()
            break


def is_same(id, sender):
    if id == str(window.ifo_user_id.text()) or sender == str(window.ifo_user_id.text()):
        return True
    else:
        return False


# 发送消息
def send(message, receiver, typecode):
    # 将要发送的信息包装为json格式并发送出去
    msg = Message(user.id, receiver, typecode, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    client.send(Tools.encode_json(msg).encode('utf-8'))


# 启动客户端
def start_client():
    print('客户端启动')
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()


# 将消息转换进消息列表中
def add_msg2list(messages, msg_list: QListWidget, text_type='left'):
    """
    messages:已处理好的消息组
    msg_list:要显示的位置
    text_type:显示格式，默认为左，传入right则为右对齐

    消息的格式如下：
    messages[0]:斜体e.g. 用户名(id) 2003-12-15 13:20:49
    messages[1~n-1]:正文消息，每行不超过30字，若超出则自动分割
    messages[n]:空行
    """
    font = QFont()
    font.setBold(True)  # 设置粗体
    font.setItalic(True)  # 设置斜体
    first_line = True
    for msg in messages:
        item = QListWidgetItem(msg)
        # 首行做出区分
        if first_line:
            item.setFont(font)
            first_line = False
        # 如果是自己发的消息，那么就用右对齐的方法显示
        if text_type == 'right':
            item.setTextAlignment(Qt.AlignRight)

        msg_list.addItem(item)


# 将消息格式化为要展示的模式
def message_format2list(text, name, time, id=''):
    if id == '':
        res = [name + ' ' + str(time)]
    else:
        res = [name + '(' + id + ') ' + str(time)]

    for i in range(0, len(text), 30):
        line = text[i:i + 30]
        res.append(line)
    res.append('')

    return res


# 向服务器发送验证请求
def is_valid_account(id, password):
    if DataBase.get_password_by_id(id) == password:
        global user
        user = DataBase.get_user_by_id(id)

        global user_id
        user_id = id
        return True


if __name__ == '__main__':
    start_client()
    # 用户GUI界面
    app = QApplication(sys.argv)

    window = GUI.MyMainForm()
    window.show()

    sys.exit(app.exec_())
