#-*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import os
import sys

from django.conf import settings
from django.core.files.uploadedfile import (
    InMemoryUploadedFile, TemporaryUploadedFile,
)
from django.core.files.uploadhandler import FileUploadHandler

from qiniu import Auth, BucketManager, put_data,put_file,urlsafe_base64_encode,PersistentFop

from lxml import etree

reload(sys)
sys.setdefaultencoding( "utf-8" )



'''
    @author:jimczj
    e-mail:jimczj@gmail.com
'''

def get_qiniu_uptoken(key,access_key=settings.QINIU_ACCESS_KEY,secret_key=settings.QINIU_SECRET_KEY,bucket=settings.QINIU_BUCKET_NAME):
    '''
        获取七牛的认证凭证
    '''


    large_saveas_key = urlsafe_base64_encode(bucket+":"+key+"-large")
    medium_saveas_key = urlsafe_base64_encode(bucket+":"+key+"-medium")
    large_ops="imageView2/2/w/970/h/970/q/100|saveas/"+large_saveas_key #设置七牛的静态持久化，参数需要跟七牛账号那里设置的一致
    medium_ops="imageView2/2/w/580/h/350/q/50|saveas/"+medium_saveas_key #具体看这个文章 http://blog.csdn.net/netdxy/article/details/50223733
    policy = {
        "persistentOps":large_ops+";"+medium_ops    
    }
    auth = Auth(access_key, secret_key)
    up_token = auth.upload_token(bucket,policy=policy)
    return up_token

def upload_content_img_to_qiniu(content):
    '''
        content参数是文章的html
        该函数会将Ueditor的图片上传到七牛，并修改图片的src属性
        最后返回修改过的content给QiniuUEditorField的get_prep_value调用
    '''
    page = etree.HTML(content)
    hrefs = page.xpath(u"//img")
    imgs_src=[href.attrib["src"] for href in hrefs]
    for img_src in imgs_src:
        if settings.QINIU_BUCKET_DOMAIN not in img_src:
            img_name='/'+img_src.split("/")[-1]
            file_path=settings.MEDIA_ROOT+img_name
            qiniu_key='/'.join(img_src.split("/")[1:])
            try:
                ret, info=put_file(up_token=get_qiniu_uptoken(key=qiniu_key),key=qiniu_key, file_path=file_path)
                if info.exception is None:
                    qiniu_file_path="http://"+settings.QINIU_BUCKET_DOMAIN+img_src
                    content=content.replace(img_src,qiniu_file_path)
                    print img_name+" upload to qiniu success "
                else:
                    print img_name+" upload to qiniu success "
            except Exception,e:
                print str(e)
                print " upload to qiniu failed "
    return content

def upload_img(img_src):
    '''
        上传封面的图片
    '''
    try:
        if settings.QINIU_BUCKET_DOMAIN not in img_src:
            img_name='/'+img_src.split("/")[-1]
            file_path=settings.MEDIA_ROOT+img_name
            qiniu_key='/'.join(img_src.split("/")[1:])

            ret, info=put_file(up_token=get_qiniu_uptoken(key=qiniu_key), key=qiniu_key,file_path=file_path)
            img_src="http://"+settings.QINIU_BUCKET_DOMAIN+img_name
            if  info.exception is None:
                print  img_name+" upload to qiniu success "
            else:
                print img_name+" upload to qiniu failed "          
    except Exception,e:
        print str(e)
        print img_name+" upload to qiniu failed "
    finally:
        return img_src

def trigger_img_persistent_fop(img_src,access_key=settings.QINIU_ACCESS_KEY,secret_key=settings.QINIU_SECRET_KEY,bucket=settings.QINIU_BUCKET_NAME):
    '''
        触发图片静态持久性操作
    '''
    try:
        if settings.QINIU_BUCKET_DOMAIN in img_src:
            key = '/'.join(img_src.split("//")[1].split("/")[1:]) #去掉 http://7xsx9g.com1.z0.glb.clouddn.com/
            q = Auth(access_key, secret_key)
            large_saveas_key = urlsafe_base64_encode(bucket+":"+key+"-large")
            medium_saveas_key = urlsafe_base64_encode(bucket+":"+key+"-medium")
            large_ops="imageView2/2/w/970/h/970/q/100|saveas/"+large_saveas_key #设置七牛的静态持久化，参数需要跟七牛账号那里设置的一致
            medium_ops="imageView2/2/w/580/h/350/q/50|saveas/"+medium_saveas_key #具体看这个文章 http://blog.csdn.net/netdxy/article/details/50223733
            ops = [large_ops,medium_ops]
            pfop = PersistentFop(q, bucket)
            ret, info = pfop.execute(key, ops, 1)
            if  info.exception is None:
                print  key+" persistent fop to success"
            else:
                print key+" persistent fop to failed"          
    except Exception,e:
        print str(e)
        print key+" persistent fop to failed"

def trigger_content_img_persistent_fop(content):
    '''
        触发文章内容图片的静态持久性操作
    '''
    page = etree.HTML(content)
    hrefs = page.xpath(u"//img")
    imgs_src=[href.attrib["src"] for href in hrefs]
    for img_src in imgs_src:
        trigger_img_persistent_fop(img_src)








