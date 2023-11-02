import datetime

# 一些无内容的信息
def error(receiver):
    return Message('0', receiver, 'ERROR', None)


def success(receiver):
    return Message('0', receiver, 'SUCCESS', None)


def fail(receiver):
    return Message('0', receiver, 'FAIL', None)


class Message:
    def __init__(self, sender, receiver, typecode, content, time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.sender = str(sender)
        self.receiver = str(receiver)
        self.typecode = str(typecode)
        self.content = str(content)
        self.time = str(time)
