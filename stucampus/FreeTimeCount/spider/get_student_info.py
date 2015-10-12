# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from sgmllib import SGMLParser

class ListName(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.is_h4 = ""
		self.name = []
	def start_option(self, attrs):
		self.is_h4 = 1
	def end_option(self):
		self.is_h4 = ""
	def handle_data(self, text):
		if self.is_h4 == 1:
			self.name.append(text)

class ListName1(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.is_h4 = ""
		self.name = []
	def start_td(self, attrs):
		self.is_h4 = 1
	def end_td(self):
		self.is_h4 = ""
	def handle_data(self, text):
		if self.is_h4 == 1:
			self.name.append(text)


url = "http://192.168.2.20/axsxx/xy.ASP"

response = urllib2.urlopen(url)
content = response.read()

content = content.decode("gb18030")
print content

obj_college = re.compile('<option value=\"(.+)\">')
college = obj_college.findall(content)
print len(college)
for index in range(0, len(college)):
	college[index] = college[index].strip()

for each_college in college:
	print each_college + ">>>"


url = 'http://192.168.2.20/axsxx/xy1.asp'

fp = open('../info/students.txt', 'w+')

for each in college:

	values = {
		'bh' : each,
		'SUBMIT' : u'查询'
	}
	for key in values.keys():
		values[key] = values[key].encode('gb18030')

	data = urllib.urlencode(values)
	#data = 'bh=2014%BC%C6%CB%E3%BB%FA%D3%EB%C8%ED%BC%FE%D1%A7%D4%BA08'
	print data

	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	content = response.read()
	content = content.decode('gb2312')
	listname = ListName()
	listname.feed(content)

	for item in listname.name:
		url1 = 'http://192.168.2.20/axsxx/xy2.asp'

		values1 = {
			'bh' : item,
			'SUBMIT' : u'查询'
		}
		for key1 in values1.keys():
			values1[key1] = values1[key1].encode('gb18030')

		data1 = urllib.urlencode(values1)
		#data = 'bh=2014%BC%C6%CB%E3%BB%FA%D3%EB%C8%ED%BC%FE%D1%A7%D4%BA08'
		print data1

		req1 = urllib2.Request(url1, data1)
		response1 = urllib2.urlopen(req1)
		content1 = response1.read()
		content1 = content1.decode('gb18030')
		listname1 = ListName1()
		listname1.feed(content1)
		for item1 in listname1.name:
			fp.write(item1.strip() + '|')
fp.close()
