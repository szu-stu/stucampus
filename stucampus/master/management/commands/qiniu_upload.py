#-*- coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from stucampus.articles.models import Article

from stucampus.custom.qiniu import upload_img
    
class Command(BaseCommand):
	'''
		@author:jimczj
    	e-mail:jimczj@gmail.com
    	执行命令python manage.py qiniu_upload时执行该函数
    	upload_img 负责将以前的封面的图片上传到七牛，而以后上传的图片，保存的时候会自动上传
		将以前的图片上传到七牛，当保存到数据库的时候，自动执行上传动作upload_content_img_to_qiniu
	'''
	def handle(self, *args, **options):
		articles=Article.objects.all()
		for article in articles:
			article.save()
		print "completed upload to qiniu"


