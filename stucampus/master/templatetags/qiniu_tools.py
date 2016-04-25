# -*- coding:utf-8 -*-
from django import template
from django.conf import settings

from lxml import etree

register = template.Library()
'''
	author:jimczj
	e-mail:jimczj@gmail.com
'''

@register.filter(name='scale_qiniu_img')
def scale_qiniu_img(url,request):
	'''
		自定义模板过滤器，使用方法{{var |scale_qiniu_img:request}}

	'''
	try:

		if request.META['HTTP_USER_AGENT'].lower().find('mobile') > 0:
			url= _transform_img_href(url,"medium")
		else:
			url= _transform_img_href(url,"large")
	except Exception,e:
		print str(e)
	finally:
		return url

@register.filter(name='scale_ueditor_img')
def scale_ueditor_img(content,request):
	'''
		自定义模板过滤器，给ueditor的字段使用,使用方法{{var |scale_ueditor_img:request}}
	'''
	if request.META['HTTP_USER_AGENT'].lower().find('mobile') > 0:
		content=_transform_content_img_href(content,"medium")
	else:
		content=_transform_content_img_href(content,"large")
	return content


def _transform_content_img_href(content,size):
	'''
		将content里面的图片src,根据设备类型替换成不同类型的src
	'''

	page=etree.HTML(content)
	hrefs=page.xpath(u"//img")
	imgs_src=[href.attrib["src"] for href in hrefs]
	for img_src in imgs_src:
		if (settings.QINIU_BUCKET_DOMAIN in img_src) and (img_src.endswith(".jpg") or img_src.endswith(".png") or img_src.endswith(".gif")):
			content=content.replace(img_src,img_src+"-"+size)
	return content

def _transform_img_href(img_src,size):
	'''
		将封面的图片src,根据设备类型替换成不同类型的src
	'''
	if (settings.QINIU_BUCKET_DOMAIN in img_src) and (img_src.endswith(".jpg") or img_src.endswith(".png") or img_src.endswith(".gif")):
		img_src=img_src.replace(img_src,img_src+"-"+size)
	elif (settings.QINIU_BUCKET_DOMAIN not in img_src) and (img_src.endswith(".jpg") or img_src.endswith(".png") or img_src.endswith(".gif")):
		img_src=img_src.replace(img_src,settings.QINIU_BUCKET_DOMAIN+img_src+"-"+size)
	return img_src
