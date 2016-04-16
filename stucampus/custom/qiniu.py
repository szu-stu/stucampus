#-*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from django.core.files.uploadedfile import (
    InMemoryUploadedFile, TemporaryUploadedFile,
)
from django.core.files.uploadhandler import FileUploadHandler

from qiniu import Auth, BucketManager, put_data,put_file

from lxml import etree



'''
    @author:jimczj
    e-mail:jimczj@gmail.com
'''

def get_qiniu_uptoken(accessKey=settings.QINIU_ACCESS_KEY,secretKey=settings.QINIU_SECRET_KEY,bucket=settings.QINIU_BUCKET_NAME):
    '''
        获取七牛的认证凭证
    '''
    auth = Auth(accessKey, secretKey)
    up_token = auth.upload_token(bucket, key=None)
    return up_token

def upload_content_img_to_qiniu(content,img=None):
    '''
        content参数是文章的html
        该函数会将Ueditor的图片上传到七牛，并修改图片的src属性
        最后返回修改过的content给QiniuUEditorField的get_prep_value调用
    '''
    page = etree.HTML(content)
    hrefs = page.xpath(u"//img")
    imgs_src=[href.attrib["src"] for href in hrefs]
    if img is not None:
        imgs_src.append(img)
    for img_src in imgs_src:
        if "http://" not in img_src:
            img_name='/'+img_src.split("/")[-1]
            file_path=settings.MEDIA_ROOT+img_name
            qiniu_key='/'.join(img_src.split("/")[1:])
            try:
                ret, info=put_file(up_token=get_qiniu_uptoken(), key=qiniu_key, file_path=file_path)
                if info.exception is None:
                    qiniu_file_path="http://"+settings.QINIU_BUCKET_DOMAIN+img_src
                    content=content.replace(img_src,qiniu_file_path)
                    print img_name+" upload to qiniu success "
                else:
                    print img_name+" upload to qiniu success "
            except Exception,e:
                print str(e)
                print img_name+" upload to qiniu failed "
    return content

def upload_img(img_src):
    '''
        上传封面的图片
    '''
    if "http://" not in img_src:
        img_name='/'+img_src.split("/")[-1]
        file_path=settings.MEDIA_ROOT+img_name
        qiniu_key='/'.join(img_src.split("/")[1:])
        try:
            ret, info=put_file(up_token=get_qiniu_uptoken(), key=qiniu_key, file_path=file_path)
            if  info.exception is None:
                print  img_name+" upload to qiniu success "
            else:
                print img_name+" upload to qiniu failed "          
        except Exception,e:
            print str(e)
            print img_name+" upload to qiniu failed "




    
            



            

