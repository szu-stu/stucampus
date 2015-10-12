# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import os
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


course_id = 0
f1 = open('../info/course_detail.txt', 'w')


url = "http://192.168.2.229/newkc/akcjj0.asp?xqh=20151"
cookiejar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
urllib2.install_opener(opener)
response = urllib2.urlopen(url)
content = response.read()
content = content.decode("gb18030")
print content

url = "http://192.168.2.229/newkc/akechengdw.asp"
response = urllib2.urlopen(url)
content = response.read()

content = content.decode("gb18030")
print content

obj_college = re.compile('<option value=\"(.+)\">')
colleges = obj_college.findall(content)
print len(colleges)
for index in range(0, len(colleges)):
	colleges[index] = colleges[index].strip()

for each_college in colleges:
	print each_college + ">>>"

url = "http://192.168.2.229/newkc/kccx.asp?flag=kkdw"


txt = open("../info/course.txt", "w")

for college in colleges:

	values = {
		'bh': college,
	}

	values['bh'] = values['bh'].encode("gb18030")
	values = urllib.urlencode(values)
	request = urllib2.Request(url, values)
	response = urllib2.urlopen(request)
	content = response.read()
	content = content.decode("gb18030")
	#print content
	#content = unicode(content, "gbk2312").encode('utf8')
	#page = open("1.html", "w")

	#page.write(content)
	#page.close()

	obj_course = re.compile('<td width=.*152.*><a href=\"(.+)\".*>(.*)</a>[.\r\n]*</td>')
	course = obj_course.findall(content)
	obj_time = re.compile("<td width=\"150\">(<small><small>)?(.*)</td>")
	time = obj_time.findall(content)

	i = 0
	for each in course:
		a = each[0].strip()
		c = each[1].strip()
		t = time[i][1].replace("<small/><small/>", "").strip()

		if t == "上课时间":
			i = i + 1
			t = time[i][1].replace("<small/><small/>", "").strip()

		txt.write(str(course_id) + "|" + c + "|" + t + "\n")

		url_students = "http://192.168.2.229/newkc/" + a;
		print url_students
		response = urllib2.urlopen(url_students)
		content = response.read().decode("gb18030")
		obj_stunos = re.compile('<td>([0-9]{10})</td>')
		stunos = obj_stunos.findall(content)

		f1.write(str(course_id))
		for stuno in stunos:
			f1.write(" " + stuno)
		f1.write("\n")

		i = i + 1

		course_id = course_id + 1



txt.close()
f1.close()
