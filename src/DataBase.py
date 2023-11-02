import os
import sqlite3

from Message import Message
from User import User

# 数据库文件路径
db_file_path = '../sources/momotalk.db'
# 确保数据库文件所在目录存在，如果不存在则创建它
db_dir = os.path.dirname(db_file_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)


# 创建message表
def init():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            typecode TEXT,
            content TEXT,
            time TEXT
        )
    ''')

    # 创建user表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            key_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT,
            password TEXT,
            name TEXT,
            sex TEXT,
            birthday TEXT,
            mail TEXT,
            info TEXT
        )
    ''')

    conn.commit()
    conn.close()


# 向信息表添加数据
def add_message(sender, receiver, typecode, content, time):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO message (sender, receiver, typecode, content, time) VALUES (?, ?, ?, ?, ?)",
                   (sender, receiver, typecode, content, time))
    conn.commit()
    conn.close()


# 删除信息表中的信息
def delete_message(message_id):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM message WHERE id=?", (message_id,))
    conn.commit()
    conn.close()


# 获取历史30条聊天记录
def get_recent_messages(limit=30):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # 查询最近的30条消息，按时间降序排列
    cursor.execute("SELECT sender, receiver, typecode, content, time FROM message ORDER BY time DESC LIMIT ?", (limit,))
    results = cursor.fetchall()

    conn.close()

    messages = []
    for result in results:
        sender, receiver, typecode, content, time = result
        message = Message(sender, receiver, typecode, content, time)
        messages.append(message)

    return messages[::-1]


# 添加用户到用户表中
def add_user(id, password, name, sex, birthday, mail, info):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (id, password, name, sex, birthday, mail, info) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (id, password, name, sex, birthday, mail, info))
    conn.commit()
    conn.close()


# 删除用户表中的用户
def delete_user(user_key_id):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE key_id=?", (user_key_id,))
    conn.commit()
    conn.close()


# 根据用户id查找用户
def get_user_by_id(user_id):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE id=?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        key_id, id, password, name, sex, birthday, mail, info = result
        user = User(id, name, sex, birthday, mail, info)
        return user
    else:
        return None  # ID不存在


# 更新密码
def update_user_password(id, new_password):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET password=? WHERE id=?", (new_password, id))
    conn.commit()
    conn.close()


# 更新用户一般信息
def update_user_info(id, name, sex, birthday, mail, info):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET name=?, sex=?, birthday=?, mail=?, info=? WHERE id=?",
                   (name, sex, birthday, mail, info, id))
    conn.commit()
    conn.close()


# 获取密码
def get_password_by_id(input_id):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # 执行查询
    cursor.execute("SELECT password FROM user WHERE id=?", (input_id,))
    result = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    if result:
        return result[0]  # 返回密码
    else:
        return None  # 没有找到匹配的ID
