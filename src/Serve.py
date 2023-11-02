import socket
import threading

import DataBase
import Message
import Tools

# 服务器配置
HOST = '127.0.0.1'
PORT = 12345

# 存储连接的客户端
clients = []

# 存储在线用户id
users = []

# 存储匿名id的列表
users_name = ["宋江", "卢俊义", "吴用", "公孙胜", "关胜", "林冲", "秦明", "呼延灼", "花荣", "柴进", "李应", "朱仝",
              "鲁智深",
              "武松", "董平", "张清", "杨志", "徐宁", "索超", "戴宗", "刘唐", "李逵", "史进", "穆弘", "雷横", "李俊",
              "阮小二", "张横", "阮小五", "张顺", "阮小七", "杨雄", "石秀", "解珍", "解宝", "燕青", "朱武", "黄信",
              "孙立",
              "宣赞", "郝思文", "韩滔", "彭玘", "单廷芳", "魏定国", "萧让", "裴宣", "欧鹏", "邓飞", "郁保四", "欧鹏",
              "段景住", "杜迁", "穆春", "焦挺", "庞万春", "韩潭", "李袁", "孔明", "孔亮", "项充", "李引", "时迁",
              "吕方",
              "杨林", "凌振", "蒋敬", "吕方", "吕梁", "吕蒙", "吕具", "孙猴子", "沙和尚", "孙行者"]


# 启动服务器
def start_server():
    # 初始化数据库
    DataBase.init()

    # 建立服务器的连接
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"服务器正在监听 {HOST}:{PORT}...")

    while True:
        # 检测客户端接入
        client_socket, client_address = server.accept()
        print(f"连接来自 {client_address}")
        clients.append(client_socket)

        # 开启客户端的事件处理线程
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


# 处理客户端消息
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                remove_client(client_socket)
                break
            # 将处理完的结果返回给客户端
            broadcast(handle_message(message), client_socket)

        except:
            continue


# 广播消息给所有客户端
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)


# 移除客户端连接
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()


# 解析从客户端接收的消息
def handle_message(message):
    # 将从客户端接收到的json信息转换回实体类
    msg = Tools.decode_json(message)

    # 根据传入的不同状态码来分别响应
    if msg.typecode == '101':  # 成功写入
        id, name, password = msg.content.split(">")
        # 向数据库添加消息
        DataBase.add_user(id, password, name, '保密', '1997-12-31', '', '这个人很懒，还什么都没有写哦')
        ans_msg = message
    elif msg.typecode == '102':  # 处理用于登录验证
        id, password = msg.content.split(">")
        if DataBase.get_password_by_id(id) == password:
            ans_msg = Tools.encode_json(Message.success(msg.sender))
        else:
            ans_msg = Tools.encode_json(Message.fail(msg.sender))

    elif msg.typecode == '201':  # 公共聊天室的聊天消息（要存储）
        ans_msg = message
        DataBase.add_message(msg.sender, msg.receiver, msg.typecode, msg.content, msg.time)
    elif msg.typecode == '202' or msg.typecode == '203':  # 匿名聊天室和私人聊天室消息都不存储
        ans_msg = message

    else:  # 出现未定义状态码时返回错误信息
        ans_msg = Message.error(msg.sender)

    return ans_msg


# 判断用户是否在线
def is_online(id):
    if id in users:
        return True
    else:
        return False


if __name__ == '__main__':
    start_server()
