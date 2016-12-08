#coding=utf-8
import hashlib
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.shortcuts import render
from wechat_sdk import WechatBasic, WechatConf
from django.http.response import HttpResponseBadRequest
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import ImageMessage
from models import KeyWord,Lottery
WECHAT_TOKEN = 'wueiz123'
AppID = 'wx2d3f8ec039af6a99'
AppSecret = '08bad122f9ade213f4496d1b45253dc6 '

conf = WechatConf(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret,
    encrypt_mode='normal',
)

wechat_instance = WechatBasic(conf=conf)
@csrf_exempt
def wechat_main(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat_instance.check_signature(
            signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponse('Verify Failed')
        return HttpResponse(request.GET.get('echostr', ''), content_type='text/plain')
    else:
        try:
            wechat_instance.parse_data(data=request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')
        wechat_instance.create_menu({
            'button':[
                {
                    'name': '圣诞礼物',
                    'sub_button': [
                        {
                            'type': 'view',
                            'name': '我要送礼',
                            'url' : 'http://stu.szu.edu.cn/christmas/'
                        },
                    ]
                },
                {
                    'type': 'view',
                    'name': 'STU.TV',
                    'url' : 'http://mp.weixin.qq.com/s/upaT7MwNgYGxM80WCMCOZA'
                }    
            ] 
        })
        message = wechat_instance.get_message()

        if isinstance(message, ImageMessage):
            openId = message.source
            if len(Lottery.objects.filter(openId = openId)):
                user = Lottery.objects.get(openId = openId)
                reply_info = u"您的抽奖码是：" + user.lottery_id
                response = wechat_instance.response_text(content=reply_info)
                return HttpResponse(response, content_type="application/xml")
            while True:
                str = random_str()
                if not len(Lottery.objects.filter(lottery_id=str)):
                    break
            user = Lottery.objects.create(openId = openId, lottery_id = str)
            reply_info = u"您的抽奖码是：" + user.lottery_id
            response = wechat_instance.response_text(content=reply_info)
            return HttpResponse(response, content_type="application/xml")
            
        reply_info = KeyWord.objects.get(keyword='default').content
        if message.type == "subscribe":
            reply_objects = KeyWord.objects.get(keyword='attention')
            reply_info = reply_objects.content
        elif message.type == 'click':
            reply_filter = KeyWord.objects.filter(keyword=message.key)
            if reply_filter:
                reply_objects = reply_filter[0]
                if reply_objects.reply_type == '1':
                    reply_info = reply_objects.content
                else:
                    reply_info = reply_objects.content
                    reply_url = reply_objects.to_url
                    reply_title = reply_objects.title
                    reply_pic = reply_objects.pic_url
                    response = wechat_instance.response_news([
                        {
                            'title': reply_title,
                            'picurl': reply_pic,
                            'description': reply_info,
                            'url': reply_url
                        }
                    ])
                    return HttpResponse(response, content_type="application/xml")
        else:
            content = message.content.strip()
            reply_filter = KeyWord.objects.filter(keyword=content)
            if reply_filter:
                reply_objects = reply_filter[0]
                if reply_objects.reply_type == '1':
                    reply_info = reply_objects.content
                else:
                    reply_info = reply_objects.content
                    reply_url = reply_objects.to_url
                    reply_title = reply_objects.title
                    reply_pic = reply_objects.pic_url
                    response = wechat_instance.response_news([
                        {
                            'title': reply_title,
                            'picurl': reply_pic,
                            'description': reply_info,
                            'url': reply_url
                        }
                    ])
                    return HttpResponse(response, content_type="application/xml")
        response = wechat_instance.response_text(content=reply_info)
        return HttpResponse(response, content_type="application/xml")


from random import Random
def random_str(randomlength=12):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str 
