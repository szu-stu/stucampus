#coding=utf-8
import hashlib
import json
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from dealmsg import replyInfo,dealcontent

from django.shortcuts import render
# Create your views here.

wechat_token = 'wueiz123'

@csrf_exempt

def wechat_main(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = wechat_token
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("hi")
        '''
        上方get部分就不做修改了- -除了欢迎关注公众号之外
        '''
    else:
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        newxml = dealxml(request_xml)
        try:
            content = dealcontent(request_xml.find('Content').text, newxml)
        except:
            content = dealcontent("hhhwww", newxml)
        return HttpResponse(replyInfo(newxml,content),content_type='application/xml')

def dealxml(xmlstr):
    """把接收到的xml消息解析"""
    msg = {}
    if xmlstr.tag == 'xml':
        for child in xmlstr:
            msg[child.tag] = smart_str(child.text)
    return msg


 
