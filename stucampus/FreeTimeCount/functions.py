# -*- coding: utf8 -*-
from django.template.response import TemplateResponse
from stucampus.FreeTimeCount.models import *
from django.http import StreamingHttpResponse
from django.shortcuts import render
import re
import string
import datetime
import json
import copy
import xlwt

def index_function(request):
	response = render(request, 'FreeTimeCount/index.html', {})
	return response


def date_function(request):
	time1_2 = []
	time3_4 = []
	time5_6 = []
	time7_8 = []
	time9_10 = []
	time11_12 = []
	week_day = None

	is_time1_2_free = True
	is_time3_4_free = True
	is_time5_6_free = True
	is_time7_8_free = True
	is_time9_10_free = True
	is_time11_12_free = True

	if request.POST:


		end_date = request.POST['date']

		start_date = datetime.datetime(2016, 9, 7)

		obj = re.compile('(\d+)-(\d+)-(\d+)')
		end_date = obj.findall(end_date)

		end_date = datetime.datetime(string.atoi(end_date[0][0]), string.atoi(end_date[0][1]), string.atoi(end_date[0][2]))
		days = (end_date - start_date).days

		week_day = end_date.strftime("%w")

		is_single_week = 1 if (days / 7) % 2 == 0 else 0

		for member in Member.objects.all():

			if member.stuID[3] != '6':
				continue

			is_time1_2_free = True
			is_time3_4_free = True
			is_time5_6_free = True
			is_time7_8_free = True
			is_time9_10_free = True
			is_time11_12_free = True

			student = Students.objects.filter(stu_no=member.stuID)
			courseTable = CourseTable.objects.filter(student=student)
			for ct in courseTable:
				courses = Course.objects.filter(course_id=ct.course_id)
				for course in courses:
					if course.weekday != '0':

						if is_single_week:
							if (course.weekday[1] == str(week_day)) and (course.weekday[0] == '0' or course.weekday[0] == '1'):
								course_time = course.time.strip("[']")
								masses = course_time.split(",")


								for mass in masses:
									if mass == '1' or mass == '2':
										is_time1_2_free = False
									if mass == '3' or mass == '4':
										is_time3_4_free = False
									if mass == '5' or mass == '6':
										is_time5_6_free = False
									if mass == '7' or mass == '8':
										is_time7_8_free = False
									if mass == '9' or mass == '10':
										is_time9_10_free = False
									if mass == '11' or mass == '12':
										is_time11_12_free = False
						else:
							if (course.weekday[1] == str(week_day)) and (course.weekday[0] == '0' or course.weekday[0] == '2'):
								course_time = course.time.strip("[']")

								masses = course_time.split(",")

								for mass in masses:
									if mass == '1' or mass == '2':
										is_time1_2_free = False
									if mass == '3' or mass == '4':
										is_time3_4_free = False
									if mass == '5' or mass == '6':
										is_time5_6_free = False
									if mass == '7' or mass == '8':
										is_time7_8_free = False
									if mass == '9' or mass == '10':
										is_time9_10_free = False
									if mass == '11' or mass == '12':
										is_time11_12_free = False
			if(len(student) != 0):

				if is_time1_2_free:
					time1_2.append(student[0].name)
				if is_time3_4_free:
					time3_4.append(student[0].name)
				if is_time5_6_free:
					time5_6.append(student[0].name)
				if is_time7_8_free:
					time7_8.append(student[0].name)
				if is_time9_10_free:
					time9_10.append(student[0].name)
				if is_time11_12_free:
					time11_12.append(student[0].name)


	else:
		print "not a post"

	if week_day == '日':
		week_day = '一'
	elif week_day == '1':
		week_day = '一'
	elif week_day == '2':
		week_day = '二'
	elif week_day == '3':
		week_day = '三'
	elif week_day == '4':
		week_day = '四'
	elif week_day == '5':
		week_day = '五'
	elif week_day == '6':
		week_day = '六'


	response = render(request, 'FreeTimeCount/date.html', {
		"time1_2" 	: ",".join(time1_2),
		"time3_4" 	: ",".join(time3_4),
		"time5_6" 	: ",".join(time5_6),
		"time7_8" 	: ",".join(time7_8),
		"time9_10"	: ",".join(time9_10),
		"time11_12"	: ",".join(time11_12),
		"week_day"	: week_day,
		"date"		: (request.POST['date'] if request.POST else None),
	})
	return response


def distribute_function(request):
	result = [[0 for i in range(6)] for j in range(7)]

	time1_2 = []
	time3_4 = []
	time5_6 = []
	time7_8 = []
	time9_10 = []
	time11_12 = []

	is_time1_2_free = True
	is_time3_4_free = True
	is_time5_6_free = True
	is_time7_8_free = True
	is_time9_10_free = True
	is_time11_12_free = True

	student_grade = {}
	result_tmp = []
	free_student = []

	if request.POST:

		if request.POST['submit'] == u"自动分配":

			for is_single_week in range(0, 2):

				for week_day in range(1, 8):

					time1_2 = []
					time3_4 = []
					time5_6 = []
					time7_8 = []
					time9_10 = []
					time11_12 = []

					is_time1_2_free = True
					is_time3_4_free = True
					is_time5_6_free = True
					is_time7_8_free = True
					is_time9_10_free = True
					is_time11_12_free = True

					for member in Member.objects.all():


						if member.stuID[3] != '6':
							continue

						is_time1_2_free = True
						is_time3_4_free = True
						is_time5_6_free = True
						is_time7_8_free = True
						is_time9_10_free = True
						is_time11_12_free = True

						student = Students.objects.filter(stu_no=member.stuID)

						if len(student) != 0:
							student_grade[student[0].name] = 0

						courseTable = CourseTable.objects.filter(student=student)
						for ct in courseTable:
							courses = Course.objects.filter(course_id=ct.course_id)
							for course in courses:
								if course.weekday != '0':

									if is_single_week:
										if (course.weekday[1] == str(week_day)) and (course.weekday[0] == '0' or course.weekday[0] == '1'):
											course_time = course.time.strip("[']")

											masses = course_time.split(",")

											for mass in masses:
												if mass == '1' or mass == '2':
													is_time1_2_free = False
												if mass == '3' or mass == '4':
													is_time3_4_free = False
												if mass == '5' or mass == '6':
													is_time5_6_free = False
												if mass == '7' or mass == '8':
													is_time7_8_free = False
												if mass == '9' or mass == '10':
													is_time9_10_free = False
												if mass == '11' or mass == '12':
													is_time11_12_free = False
									else:
										if (course.weekday[1] == str(week_day)) and (course.weekday[0] == '0' or course.weekday[0] == '2'):
											course_time = course.time.strip("[']")

											masses = course_time.split(",")

											for mass in masses:
												if mass == '1' or mass == '2':
													is_time1_2_free = False
												if mass == '3' or mass == '4':
													is_time3_4_free = False
												if mass == '5' or mass == '6':
													is_time5_6_free = False
												if mass == '7' or mass == '8':
													is_time7_8_free = False
												if mass == '9' or mass == '10':
													is_time9_10_free = False
												if mass == '11' or mass == '12':
													is_time11_12_free = False

						if len(student) != 0:

							if is_time1_2_free:
								time1_2.append(student[0].name)
							if is_time3_4_free:
								time3_4.append(student[0].name)
							if is_time5_6_free:
								time5_6.append(student[0].name)
							if is_time7_8_free:
								time7_8.append(student[0].name)
							if is_time9_10_free:
								time9_10.append(student[0].name)
							if is_time11_12_free:
								time11_12.append(student[0].name)

					if is_single_week == 0:

						result[week_day - 1][0] = time1_2
						result[week_day - 1][1] = time3_4
						result[week_day - 1][2] = time5_6
						result[week_day - 1][3] = time7_8
						result[week_day - 1][4] = time9_10
						result[week_day - 1][5] = time11_12
					else:
						for each_student in time1_2:
							if each_student not in result[week_day - 1][0]:
								result[week_day - 1][0].append(each_student + u"(单周)")
						for each_student in time3_4:
							if each_student not in result[week_day - 1][1]:
								result[week_day - 1][1].append(each_student + u"(单周)")
						for each_student in time5_6:
							if each_student not in result[week_day - 1][2]:
								result[week_day - 1][2].append(each_student + u"(单周)")
						for each_student in time7_8:
							if each_student not in result[week_day - 1][3]:
								result[week_day - 1][3].append(each_student + u"(单周)")
						for each_student in time9_10:
							if each_student not in result[week_day - 1][4]:
								result[week_day - 1][4].append(each_student + u"(单周)")
						for each_student in time11_12:
							if each_student not in result[week_day - 1][5]:
								result[week_day - 1][5].append(each_student + u"(单周)")


						for index,each_student in enumerate(result[week_day - 1][0]):
							if each_student.replace(u"(单周)", "") not in time1_2:
								result[week_day - 1][0][index] = result[week_day - 1][0][index] + u"(双周)"
						for index,each_student in enumerate(result[week_day - 1][1]):
							if each_student.replace(u"(单周)", "") not in time3_4:
								result[week_day - 1][1][index] = result[week_day - 1][1][index] + u"(双周)"
						for index,each_student in enumerate(result[week_day - 1][2]):
							if each_student.replace(u"(单周)", "") not in time5_6:
								result[week_day - 1][2][index] = result[week_day - 1][2][index] + u"(双周)"
						for index,each_student in enumerate(result[week_day - 1][3]):
							if each_student.replace(u"(单周)", "") not in time7_8:
								result[week_day - 1][3][index] = result[week_day - 1][3][index] + u"(双周)"
						for index,each_student in enumerate(result[week_day - 1][4]):
							if each_student.replace(u"(单周)", "") not in time9_10:
								result[week_day - 1][4][index] = result[week_day - 1][4][index] + u"(双周)"
						for index,each_student in enumerate(result[week_day - 1][5]):
							if each_student.replace(u"(单周)", "") not in time11_12:
								result[week_day - 1][5][index] = result[week_day - 1][5][index] + u"(双周)"





			result_tmp = copy.deepcopy(result)

			for i in range(0, 5):
				for j in range(1, 4):
					for each_student in result[i][j]:
						if each_student.find("(") != -1:
							each_student = each_student.replace(u"(双周)", "")
							each_student = each_student.replace(u"(单周)", "")
							student_grade[each_student] = student_grade[each_student] + 0.5
						else:
							student_grade[each_student] = student_grade[each_student] + 1

			for key in student_grade:
				print key + "=" + str(student_grade[key])

			selected_student = []

			tmp = []

			for i in range(0,5):
				for j in range(1, 4):
					tmp.append((i, j, len(result[i][j])))

			#sort

			for i in range(0, len(tmp)):
				for j in range(i + 1, len(tmp)):
					if tmp[i][2] > tmp[j][2]:
						tmp[i],tmp[j] = tmp[j],tmp[i]

			for i in range(0, 5):
				for j in range(1, 4):
					for m in range(0, len(result[i][j])):
						for n in range(m + 1, len(result[i][j])):
							tmp_m = result[i][j][m].replace(u"(双周)", "")
							tmp_m = tmp_m.replace(u"(单周)", "")
							tmp_n = result[i][j][n].replace(u"(双周)", "")
							tmp_n = tmp_n.replace(u"(单周)", "")
							if student_grade[tmp_m] > student_grade[tmp_n]:
								result[i][j][m],result[i][j][n] = result[i][j][n], result[i][j][m]

			print tmp

			#distribute

			for i in range(0, len(tmp)):
				if len(result[tmp[i][0]][tmp[i][1]]) <= 1:
					for each in result[tmp[i][0]][tmp[i][1]]:
						tmp_each = each.replace(u"(双周)", "")
						tmp_each = tmp_each.replace(u"(单周)", "")
						if tmp_each not in selected_student:
							selected_student.append(tmp_each)

				else:
					count = 0
					tmp_list = []
					for each in result[tmp[i][0]][tmp[i][1]]:
						tmp_each = each.replace(u"(双周)", "")
						tmp_each = tmp_each.replace(u"(单周)", "")
						if tmp_each not in selected_student:

							if count == 1:
								if (each.find(u"(双周)") != -1 and tmp_list[0].find(u"(双周)") != -1) or (each.find(u"(单周)") != -1 and tmp_list[0].find(u"(单周)") != -1):
									continue

							selected_student.append(tmp_each)
							tmp_list.append(each)
							count = count + 1

						if count == 4:#set student num
							break

					result[tmp[i][0]][tmp[i][1]] = tmp_list

			for i in range(0, 5):
				result[i][0] = []



			for member in Member.objects.all():
				student = Students.objects.filter(stu_no=member.stuID)
				if len(student) != 0:
					if (student[0].name not in selected_student) and student[0].stu_no[3] == '4':
						free_student.append(student[0].name)

			book = xlwt.Workbook(encoding='utf-8', style_compression=0)
			sheet1 = book.add_sheet(u"值班表", cell_overwrite_ok=True)
			sheet2 = book.add_sheet(u"参考", cell_overwrite_ok=True)

			style = xlwt.easyxf('align: wrap on')

			text = [u'课程表', u'星期一', u'星期二', u'星期三', u'星期四', u'星期五']

			for index,each in enumerate(text):
				sheet1.write(0, index, each, style)
				sheet2.write(0, index, each, style)
				sheet1.col(index).width = 10000
				sheet2.col(index).width = 10000

			text = [u'第1、2节', u'第3、4节', u'第5、6节', u'第7、8节']

			for index,each in enumerate(text):
				sheet1.row(index + 1).height = 500
				sheet2.row(index + 1).height = 2000
				sheet1.write(index + 1, 0, each, style)
				sheet2.write(index + 1, 0, each, style)
				for i in range(0, 5):
					sheet1.write(index + 1, i + 1, ",".join(result[i][index]), style)
					sheet2.write(index + 1, i + 1, ",".join(result_tmp[i][index]), style)

			book.save("stucampus/FreeTimeCount/info/distribute.xls")



		else:
			def file_iterator(file_name, chunk_size=512):
			    with open(file_name) as f:
			      while True:
			        c = f.read(chunk_size)
			        if c:
			          yield c
			        else:
			          break


			the_file_name = "stucampus/FreeTimeCount/info/distribute.xls"
			response = StreamingHttpResponse(file_iterator(the_file_name))
			response['Content-Type'] = 'application/octet-stream'
			response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

  			return response
	else:
		print "not a post"

	print result_tmp

	response = render(request, 'FreeTimeCount/distribute.html', {"result" : json.dumps(result), "result_tmp" : json.dumps(result_tmp), "free_student" : json.dumps(free_student)})
	return response

def member_function(request):
	courseTable = None
	student = None
	courses = []

	if request.POST:

		name = request.POST['name'].strip()
		number = request.POST['number'].strip()



		if len(name) != 0:
			student = Students.objects.filter(name=name)
			courseTable = CourseTable.objects.filter(student=student)
			for ct in courseTable:
				courses.append(Course.objects.filter(course_id=ct.course_id))

		elif len(number) != 0:
			student = Students.objects.filter(stu_no=number)
			courseTable = CourseTable.objects.filter(student=student)
			for ct in courseTable:
				courses.append(Course.objects.filter(course_id=ct.course_id))


	else:
		print 'not a post request'

	response = render(request, 'FreeTimeCount/member.html', {"students": student, "courses": courses, "len": (len(student) if student != None else 0)})
	return response

def insert_function(request):
	Students.objects.all().delete()
	Course.objects.all().delete()
	CourseTable.objects.all().delete()

	# Step1
	file = open("stucampus/FreeTimeCount/info/students.txt", "r")
	content = file.read()
	file.close()

	pieces = content.split("|")

	i = 2
	c = 5
	index = 1
	query_set_list = []
	while i < len(pieces):
		if len(pieces[i].strip()) != 0:
			c = c + 1
		if c == 6:
			c = 0
			print pieces[i]

			if pieces[i - 1] != u'学号':
				index = index + 1
				try:
					s = Students(id=index, stu_no=pieces[i - 1], name=pieces[i], sex=pieces[i + 1], major=pieces[i + 2],college=pieces[i + 3])
					query_set_list.append(s)
				except:
					print "error"





		i = i + 1

	Students.objects.bulk_create(query_set_list)


	# Step2
	file = open("stucampus/FreeTimeCount/info/course.txt", "r")
	content = file.read()
	file.close()

	pieces = content.split("\n")


	query_set_list = []
	index = 1

	for piece in pieces:

		print "piece=" + piece

		if len(piece) == 0:
			continue

		weekday = "0"
		time = "0"
		mass = piece.split("|")

		id = string.atoi(mass[0])
		course_name = mass[1]

		if mass[2] == "." or len(mass) == 2 or len(mass[2]) == 0:
			print "the time session is empty"
			s =  Course(id=index, course_id=id, weekday=weekday, course_name=course_name, time=time, place="wenkelou")
			index = index + 1
			#print "id=" + str(id + 1)
			query_set_list.append(s)
		else:
			print "mass[2]=" + mass[2]

			masses = mass[2].split(";");

			for m in masses:
				if m.find('单') != -1:
					weekday = "1"
				elif m.find('双') != -1:
					weekday = "2"
				else:
					weekday = "0"

				if m.find('一') != -1:
					weekday = weekday + "1"
				elif m.find('二') != -1:
					weekday = weekday + "2"
				elif m.find('三') != -1:
					weekday = weekday + "3"
				elif m.find('四') != -1:
					weekday = weekday + "4"
				elif m.find('五') != -1:
					weekday = weekday + "5"
				elif m.find('六') != -1:
					weekday = weekday + "6"
				elif mass.find('日') != -1:
					weekday = weekday + "7"

				print "weekday=" + str(weekday)

				obj = re.compile('([,0-9]+)')
				time = obj.findall(m)
				s =  Course(id=index, course_id=id, weekday=weekday, course_name=course_name, time=time, place="wenkelou")
				index = index + 1
				#print "id=" + str(id + 1)
				query_set_list.append(s)


	Course.objects.bulk_create(query_set_list)





	#Step3

	file = open("stucampus/FreeTimeCount/info/course_detail.txt", "r")
	content = file.read()
	file.close()

	index = 1
	query_set_list = []

	pieces = content.split("\n")

	for student in Students.objects.all():
		print student.name

		for piece in pieces:

			if len(piece) == 0:
				break

			if piece.find(student.stu_no) != -1:
				mass = piece.split(" ")
				ct = CourseTable(id=index, student=student, course_id=mass[0])
				index = index + 1
				query_set_list.append(ct)

	CourseTable.objects.bulk_create(query_set_list)

	Member.objects.all().delete()

        student_list_rander = ["2016080031","2016020403","2016200036","2016020089","2016154069","2016150175","2016140007","2016190098","2016154039","2016150187","2016110156","2016190108","2016150055","2016150189","2016154119","2016040307","2016150011","2016150068","2016150106","2016150043","2016170125","2015150077","2015150101","2016180092","2016154093","2016222002","2016150083","2016154110","2016154074","2016154003","2016150097","2016154080","2016200065","2015130257","2016154103","2016150163","2016222042","2016080059","2016154099","2016154083","2016180023","2016190070","2016110064","2016090131","2016154091","2016154044","2016190095","2016080034","2016080069","2016102035","2016304106","2016080133","2016102047","2015101015","2016224004","2016102025","2016085085","2015020494","2015071025","2016101088","2016113104","2016071057","2016150001","2016150150","2016154038","2016080134","2016080065","2016042161","2016150148","2016114054","2016160047","2016073016","2016190104","2016101019","2016113097","2016242023","2016010119","2016085010","2016010137","2016150057","2016242030","2016154046","2016200004","2016080101","2016154114","2016080040","2016031214","2016180022"]
	#m = Member(stuID="2015080217"); m.save()
        for student_id_r in student_list_rander:
            m = Member(stuID=student_id_r)
            m.save()
	#m = Member(stuID="2015072051"); m.save()
	#m = Member(stuID="2015072056"); m.save()
	#m = Member(stuID="2015150027"); m.save()
	#m = Member(stuID="2015071107"); m.save()
	#m = Member(stuID="2015150145"); m.save()
	#m = Member(stuID="2015150104"); m.save()
	#m = Member(stuID="2015072050"); m.save()
	#m = Member(stuID="2015072007"); m.save()
	#m = Member(stuID="2015080003"); m.save()
	#m = Member(stuID="2015040477"); m.save()
	#m = Member(stuID="2015072070"); m.save()
	#m = Member(stuID="2015150063"); m.save()
	#m = Member(stuID="2015150007"); m.save()
	#m = Member(stuID="2015150288"); m.save()
	#m = Member(stuID="2015150033"); m.save()
	#m = Member(stuID="2015150324"); m.save()
	#m = Member(stuID="2015150124"); m.save()
	#m = Member(stuID="2015150246"); m.save()
	#m = Member(stuID="2015150304"); m.save()
	#m = Member(stuID="2015150258"); m.save()
	#m = Member(stuID="2015160196"); m.save()
	#m = Member(stuID="2015150122"); m.save()
	#m = Member(stuID="2015150058"); m.save()
	#m = Member(stuID="2015130046"); m.save()
	#m = Member(stuID="2015150006"); m.save()
	#m = Member(stuID="2015150166"); m.save()
	#m = Member(stuID="2015150049"); m.save()
	#m = Member(stuID="2015150218"); m.save()
	#m = Member(stuID="2015150321"); m.save()
	#m = Member(stuID="2015150301"); m.save()
	#m = Member(stuID="2015150320"); m.save()
	#m = Member(stuID="2015080194"); m.save()
	#m = Member(stuID="2015150287"); m.save()
	#m = Member(stuID="2015072058"); m.save()
	#m = Member(stuID="2015140172"); m.save()
	#m = Member(stuID="2015242049"); m.save()
	#m = Member(stuID="2015010150"); m.save()
	#m = Member(stuID="2015241039"); m.save()
	#m = Member(stuID="2015020441"); m.save()
	#m = Member(stuID="2015080084"); m.save()
	#m = Member(stuID="2015150182"); m.save()
	#m = Member(stuID="2015050158"); m.save()
	#m = Member(stuID="2015010141"); m.save()
	#m = Member(stuID="2015150126"); m.save()
	#m = Member(stuID="2015150249"); m.save()
	#m = Member(stuID="2015012051"); m.save()
	#m = Member(stuID="2015110037"); m.save()
	#m = Member(stuID="2015080004"); m.save()
	#m = Member(stuID="2015040478"); m.save()
	#m = Member(stuID="2015160024"); m.save()
	#m = Member(stuID="2015080086"); m.save()
	#m = Member(stuID="2015200013"); m.save()
	#m = Member(stuID="2015080134"); m.save()
	#m = Member(stuID="2015140094"); m.save()
	#m = Member(stuID="2015160009"); m.save()
	#m = Member(stuID="2015200027"); m.save()
	#m = Member(stuID="2015150032"); m.save()
	#m = Member(stuID="2015150181"); m.save()
	#m = Member(stuID="2015140096"); m.save()
	#m = Member(stuID="2015080171"); m.save()
	#m = Member(stuID="2015160022"); m.save()
	#m = Member(stuID="2015150073"); m.save()
	#m = Member(stuID="2015150259"); m.save()
	#m = Member(stuID="2015140166"); m.save()
	#m = Member(stuID="2015140191"); m.save()

	print "Done."



	response = render(request, 'FreeTimeCount/distribute.html', {})
	return response
