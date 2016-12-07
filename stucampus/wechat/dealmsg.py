#coding=utf-8

import time
from .models import KeyWord as kw
from .models import Lottery as lo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def replyInfo(msg,content):
    reply = '''
            <xml>
            <ToUserName>%s</ToUserName>
            <FromUserName>%s</FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType>%s</MsgType>
            <Content>%s</Content>
            <FuncFlag>0</FuncFlag>
            </xml>'''
    xml = reply % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text',  content)
    return xml

def dealcontent(content, msg):
    if( content == 'hhhwww'):
        openId =  msg['FromUserName']
        if len(lo.objects.filter(openId = openId)):
            user = lo.objects.get(openId = openId)
            return u"您的抽奖码是：" + user.lottery_id
        while True:
            str = random_str()
            if not len(lo.objects.filter(lottery_id=str)):
                break
        user = lo.objects.create(openId = openId, lottery_id = str)
        return u"您的抽奖码是" + user.lottery_id
    else:
        return u"嗯"


from random import Random
def random_str(randomlength=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
