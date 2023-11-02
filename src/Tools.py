import json
import random

import DataBase
from Message import Message


def json2Message(d):
    return Message(d['sender'], d['receiver'], d['typecode'], d['content'], d['time'])


def decode_json(message):
    return json.loads(message, object_hook=json2Message)


def encode_json(message):
    return str(json.dumps(obj=message.__dict__))


def generate_new_id():
    while True:
        # 生成一个6位账号，其中首位不为0
        number = random.randint(100000, 999999)
        # 与数据库中账号数据进行检测对比
        if str(number)[0] != '0' and (DataBase.get_user_by_id(str(number)) is None):
            return str(number)
