#-*- coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from stucampus.articles.models import Article
from stucampus.custom.qiniu import trigger_img_persistent_fop, trigger_content_img_persistent_fop

    
class Command(BaseCommand):
	'''
		@author:jimczj
    	e-mail:jimczj@gmail.com
    	执行命令python manage.py qiniu_persistent_fop时执行该函数
    	触发七牛静态持久化操作
	'''
	def handle(self, *args, **options):
		articles=Article.objects.all()
		for article in articles:
			if article.content:
				trigger_content_img_persistent_fop(unicode(article.content))
			if article.cover:
				trigger_img_persistent_fop(unicode(article.cover))
		print "completed upload to qiniu"


