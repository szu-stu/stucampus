#coding:utf-8
import requests
import base64
import random
import re

from bs4 import BeautifulSoup

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from models import Professions, Plan, Courses, MCCourses


# 在当前目录下创建可能的双专业个人信息
import os
DEBUG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DEBUG")

import traceback

class CreditStatistics(object):
	def __init__(self, stuNum, stuPwd, captcha, cookies):
		self.stuNum = stuNum
		self.stuPwd = stuPwd
		self.captcha = captcha
		self.cookies = {
			cookies[:cookies.find("=")]: cookies[cookies.find("=") + 1:cookies.find(";")]
		}

		self.grade = None
		self.college = None
		self.profession = None
		self.professionId = None

		self.minorType = None # 辅修类别
		self.minorGrade = None # 双学位/辅修
		self.minorCollege = None # 双学位/辅修
		self.minorProfession = None # 双学位/辅修
		self.minorProfessionId = None # 双学位/辅修 专业Id

		self.plan = None
		self.programUrl = [] # 用到的培养方案的url

		self.__init__changeProfession()

		self._finish = False
		self._success = False
		self._errorInfo = None
		self._latestSelectionResultUrl = None
		self._repairedCoursesUrl = None

		self._currentHtml = ""

		self._start()

	def __init__changeProfession(self):
		'''
			初始化与更换专业需要重新初始化的变量
		'''
		self.latestSelectionResult = [] #最新选课结果
		self.repairedCourses = [] #已修课程
		self.failCourses = [] #挂科课程

		self.repairedPublicCourses = [] # 已修公共课程
		self.repairedProfessionCourses = [] # 已修学科专业核心课程
		self.repairedProfessionElective = [] # 已修学科选修课程
		self.repairedElective = [] # 已修（除学科专业）选修课程
		self.repairedDoubleCourses = [] # 双学位/双专业 课程
		self.nonRepairedPublicCourses = [] #未修公共课程
		self.nonRepairedProfessionCourses = [] # 未修学科专业核心课程
		self.optionalCourses = [] # 可选修课程
		self.nonRepairedDoubleCourses = [] # 双学位/双专业 课程

		self.uncertainCourses = [] # 未在培养方案中查找到的必修课程

	def _getLatestSelectionResult(self):
		'''
			获取最新选课结果
		'''
		url = self._latestSelectionResultUrl
		response = requests.get(url, cookies=self.cookies)

		self._currentHtml = response.content

		html = BeautifulSoup(response.content, "lxml")
		# table = html.find(id="zxxkjgTable")
		table = html.find_all("table")
		if len(table) < 2:
			# 选课结果为空
			return 
		table = table[1]
		trs = table.find_all("tr")[1:] # 除去第一个表头

		# 判断最新选课结果的成绩是否已出
		if len(self.repairedCourses) > 0:
			if self.repairedCourses[len(self.repairedCourses) - 1]["termNum"] == trs[0].find_all("td")[1].string:
					# 成绩已出的话就不添加最新选课结果
					return 
		if len(trs) > 0:
			tableType = len(trs[0].find_all("td")) - 11 #判断最新选课结果包不包含培养方案认定课程类型，包含则tableType = 1, 否则为0
		else :
			return ;
		for tr in trs:
			td = tr.find_all("td")
			data = {
				"termNum": td[1].string.strip(),
				"courseNum": td[2].string.strip()[:-2], # 从课程号中除去班级信息
				"courseType": td[3 + tableType].string.strip(),
				"courseName": td[4 + tableType].string.strip(),
				"credit": float(td[5 + tableType].string.strip()),
				"creditType": "无"
			}
			matchCourse = self._inCourseInCourseList(data, self.failCourses, "courseNum", "courseName");
			if matchCourse:
				self.failCourses.remove(matchCourse)
			self.latestSelectionResult.append(data)

	def _getRepairedCourses(self):
		'''
			获取已修课程，并分离出挂科科目
		'''
		url = self._repairedCoursesUrl
		response = requests.get(url, cookies=self.cookies)

		self._currentHtml = response.content

		html = BeautifulSoup(response.content, "lxml")
		tables = html.find_all("table")
		for x in xrange(1, len(tables), 3):
			table = tables[x]
			trs = table.find_all("tr")[1:] #不要表头
			infoType = len(trs[0].find_all("td")) - 11# 2015年第一学期表头没有培养方案认定课程类别 标记infoType为0 含培养方案认定课程类别标记为1
			for tr in trs:
				td = tr.find_all("td")
				data = {
					"termNum": td[1].string.strip(),
					"courseNum": td[2].string.strip()[:-2], # 从课程号中除去班级信息
					"courseName": td[3].string.strip(),
					"courseType": td[4 + infoType].string.strip(),
					"credit": float(td[5 + infoType].string.strip()),
					"creditType": "无"
				}
				creditGet = float(td[6 + infoType].string)
				if creditGet == 0: # 取得学分为0 说明挂科
					self.failCourses.append(data)
				else :
					matchCourse = self._inCourseInCourseList(data, self.failCourses, "courseNum", "courseName");
					if matchCourse:
						self.failCourses.remove(matchCourse)
					self.repairedCourses.append(data)

	@staticmethod
	def getCaptcha():
		'''
			获取验证码图片临时地址
			@return (string, string) (图片base64数据, cookies)
		'''
		codeUrl = "http://192.168.2.20/mycode/code.asp?id=!!!&random=" + str(random.random())
		response = requests.get(codeUrl)
		cookies = response.headers["Set-cookie"]
		return (base64.b64encode(response.content), cookies)

	def _login(self):
		'''
			登录学生信息查询系统
		'''
		url = "http://192.168.2.20/axsxx/AALICENSEstd.asp"
		params = {
			"USERID": self.stuNum,
			"PASSWORD": self.stuPwd,
			"GetCode": self.captcha,
			"SUBMIT": "确 定"
		}
		response = requests.post(url, data=params, cookies=self.cookies)

		self._currentHtml = response.content
		# 登录成功返回 <script>top.location.href='../Amain.asp';</script>
		if response.content.find("top.location.href=") == -1:
			print "用户名或口令错误 in _login"
			raise Exception("用户名或口令错误")

	def _getBasicInfo(self):
		'''
			获取年级、学院、专业
			@return boolean 获取是否成功
		'''
		url = "http://192.168.2.20/AXSXX/xjxxcheck.aspx"
		params = {
			"stulogflag": True,
			"cetlogflag": True,
			"USERID": "",
			"PASSWORD": self.stuPwd,
			"GetCode": self.captcha,
			"userxhSTD": self.stuNum,
			"useridSTD":self.stuNum,
			"userpms": "S",
			"level": 0,
			"PMSFILEC": "/AXSXX/aipconstd.asp",
			"PMSFILEM": "AXSXX/xjxxcheck.asp",
			"StuXjxxcheck": 1
		}
		response = requests.post(url, data=params, cookies=self.cookies)

		self._currentHtml = response.content

		html = BeautifulSoup(response.content, "lxml")
		# 判断招生高考信息是否为空判断是否登录成功
		if html.find(id="lblKsh").string == None:
			print "用户名或口令错误 in _getBasicInfo"
			raise Exception("用户名或口令错误")

		cookies = response.headers["Set-cookie"]
		self.cookies["ASP.NET_SessionId"] = cookies[cookies.find("=") + 1:cookies.find(";")]
		
		self.grade = int(html.find(id="lblNj").string.strip())
		self.college = html.find(id="lblXy").string.strip()
		
		profession = html.find(id="lblZxzy").string.strip()
		if profession.find("  ") != -1:
			# 双专业或双学位
			# 计算机与软件学院  数学与计算机科学实验班
			# 计算机科学与技术（数学与计算机科学实验班）
			# http://192.168.2.20/axsxx/sxwfx_zige.asp 双专业/双学位/辅修资格
			profession = profession.replace("  ", "（") + "）"
		else:
			# 查询是否为双专业为双学位
			self._getMinorInfo()
		self.profession = profession

	def _getMinorInfo(self):
		'''
			获取双学位辅修信息
		'''
		url = "http://192.168.2.20/axsxx/sxwfx_zige.asp"
		response = requests.get(url, cookies=self.cookies)

		self._currentHtml = response.content

		if response.content == "":
			# 为空说明不是双修或双学位
			return 
		html = BeautifulSoup(response.content, "lxml")
		td = html.form.table.find_all(width="60%")
		self.minorGrade = int(td[1].string)
		self.minorProfession = td[2].font.string.strip()
		self.minorType = td[3].font.string.strip()
		self.minorCollege = td[5].string.strip()

		self._getMinorProfessionId()

	def _getRelativeUrl(self):
		'''
			获取最新选课结果和各学期成绩的url
		'''
		url = "http://192.168.2.20/AXSXX/aipconstd.asp"
		response = requests.get(url, cookies=self.cookies)

		self._currentHtml = response.content

		html = BeautifulSoup(response.content, "lxml")
		aLabels = html.find_all("a")
		for a in aLabels:
			for aText in a.strings:
				if aText == "最新选课情况":
					self._latestSelectionResultUrl = "http://192.168.2.20/AXSXX/" + a["href"]
					break
				elif aText == "各学期成绩":
					self._repairedCoursesUrl = "http://192.168.2.20/AXSXX/" + a["href"]
					break
		if self._latestSelectionResultUrl == None or self._repairedCoursesUrl == None:
			raise Exception("获取最新选课页面URL失败")

	def _getProfessionId(self):
		'''
			通过已获取的信息查询数据库获得专业id
		'''
		query = Professions.objects.filter(grade=self.grade).filter(college=self.college)
		if len(query) == 0:
			raise Exception("查询不到专业id")
		profession = query.filter(profession=self.profession)
		if len(profession) == 0:
			profession = query.filter(profession__contains=self.profession)
			if len(profession) == 0:
				self.profession = self.college
				profession = query[0]
			else :
				profession = profession[0]
		else :
			profession = profession[0]

		self.professionId = profession.id
		self.programUrl.append(profession.url)

	def _getMinorProfessionId(self):
		'''
			获取双修双学位专业id
		'''
		query = Professions.objects.filter(grade=self.minorGrade).filter(college=self.minorCollege).filter(profession=self.minorProfession)
		if len(query) < 1:
			raise Exception("查询不到双学位或者双修专业id")
		self.minorProfessionId = query[0].id
		self.programUrl.append(query[0].url)

	def _getPlan(self):
		query = Plan.objects.filter(professionId=self.professionId)
		if len(query) < 1:
			raise Exception("专业id不存在！")
		query = query[0]
		artsStream = query.artsStream if query.artsStream else 0.0
		scienceStream = query.scienceStream if query.scienceStream else 0.0
		self.plan = {
			"publicRequired": query.publicRequired,
			"professionalRequired": query.professionalRequired,
			"elective": query.elective,
			"professionalElective": query.professionalElective,
			"artsStream": artsStream,
			"scienceStream": scienceStream,
			"practice": query.practice,
			"minorRemark": query.minorRemark,
			"doubleRemark": query.doubleRemark
		}

	def _getCourses(self):
		'''
			通过专业id查询该专业的所有课程
		'''
		query = Courses.objects.filter(professionId=self.professionId)
		for course in query:
			courseType = course.courseType
			data = self._querySetToDic(course)
			if courseType == "公共必修课":
				self.nonRepairedPublicCourses.append(data)
			elif courseType == "学科专业核心课":
				self.nonRepairedProfessionCourses.append(data)
			elif courseType == "学科专业选修课":
				self.optionalCourses.append(data)
		
		# 获取本学院其他专业非限选专业选修课程
		professes = Professions.objects.filter(grade=self.grade).filter(college=self.college)
		for profess in professes:
			if profess.id == self.professionId:
				continue
			query = Courses.objects.filter(professionId=profess.id).filter(courseType="学科专业选修课")
			for course in query:
				if course.remark == "限选":
					continue
				data = self._querySetToDic(course)
				if not data in self.optionalCourses:
					self.optionalCourses.append(data)

		if self.minorProfessionId:
			# 获取双修/双学位课程
			query = Courses.objects.filter(professionId=self.minorProfessionId).filter(courseType__contains=self.minorType)
			for course in query:
				data = self._querySetToDic(course)
				self.nonRepairedDoubleCourses.append(data)

	def _retakeCourses(self):
		'''
			从挂科课程列表中找出未重修的课程，添加到新的挂科列表
		'''
		failCourses = []
		for failCourse in self.failCourses:
			if not (failCourse in self.repairedCourses or failCourse in self.latestSelectionResult):
				# 挂科科目不在已修课程中，课程添加到挂科课程列表
				failCourses.append(failCourse)
		self.failCourses = failCourses

	def _matchAllCourses(self):
			self._matchCourses(self.latestSelectionResult) # 匹配最新选课结果
			self._matchCourses(self.repairedCourses) # 匹配已修课程

	def _matchCourses(self, courseList):
		for course in courseList:
			find = False
			if course["courseNum"][:2] == "MC": #判断是否为MOOC课程
				self._matchMCCourse(course)
			elif course["courseNum"][:5] == "53000": # 判断是否为体育课， 体育课前五位为53000
				self._matchPECourse(course)
			else :
				self._matchOtherCourse(course)

	def _matchMCCourse(self, course):
		'''
			MOOC课程匹配
			通过匹配课程名
		'''
		query = MCCourses.objects.filter(courseName=course["courseName"])
		if len(query) < 1:
			print "MOOC课程" + course["courseName"] + "未记录在数据库"
			# 不在的话...先放进选修列表中
			self.repairedElective.append(course)
			return
		query = query[0]
		course["creditType"] = query.creditType

		matchResult = CreditStatistics._inCourseInCourseList(course, self.nonRepairedPublicCourses, "courseName")
		if matchResult:# 判断是否在公共必修课程
			self.repairedPublicCourses.append(course)
			self.nonRepairedPublicCourses.remove(matchResult)
			return 
		matchResult = CreditStatistics._inCourseInCourseList(course, self.nonRepairedProfessionCourses, "courseName")
		if matchResult:# 判断是否在专业必修课程
			self.repairedProfessionCourses.append(course)
			self.nonRepairedProfessionCourses.remove(matchResult)
			return
		matchResult = CreditStatistics._inCourseInCourseList(course, self.optionalCourses, "courseName")
		if matchResult: # 判断是否在专业选修课程
			self.repairedProfessionElective.append(course)
			self.optionalCourses.remove(matchResult)
			return
		matchResult = CreditStatistics._inCourseInCourseList(course, self.nonRepairedDoubleCourses, "courseName")
		if matchResult: # 判断是否在双专业/辅修课程中
			course["creditType"] = matchResult["creditType"]
			self.repairedDoubleCourses.append(course)
			self.nonRepairedDoubleCourses.remove(course)
			return
		# 都不在的话...放进选修列表中
		self.repairedElective.append(course)

	def _matchPECourse(self, course):
		'''
			体育课程匹配
		'''
		for publicCourse in self.nonRepairedPublicCourses:
			if publicCourse["courseNum"][:5] == "53000":
				self.repairedPublicCourses.append(course)
				self.nonRepairedPublicCourses.remove(publicCourse)

	def _matchOtherCourse(self, course):
		'''
			匹配除MOOC和体育课程以外的课
		'''
		matchResult = CreditStatistics._inCourseInCourseList(course, self.nonRepairedPublicCourses, "courseNum", "courseName")
		if matchResult:# 判断是否在公共必修课程
			self.repairedPublicCourses.append(course)
			self.nonRepairedPublicCourses.remove(matchResult)
			return 
		matchResult = CreditStatistics._inCourseInCourseList(course, self.nonRepairedProfessionCourses, "courseNum", "courseName")
		if matchResult:# 判断是否在专业必修课程
			course["creditType"] = matchResult["creditType"]
			self.repairedProfessionCourses.append(course)
			self.nonRepairedProfessionCourses.remove(matchResult)
			return 
		matchResult = CreditStatistics._inCourseInCourseList(course, self.optionalCourses, "courseNum", "courseName")
		if matchResult: # 判断是否在专业选修课程
			course["creditType"] = matchResult["creditType"]
			self.repairedProfessionElective.append(course)
			self.optionalCourses.remove(matchResult)
			return
		matchResult = CreditStatistics._inCourseInCourseList(course, self.nonRepairedDoubleCourses, "courseNum", "courseName")
		if matchResult: # 判断是否在双专业/辅修课程中
			course["creditType"] = matchResult["creditType"]
			self.repairedDoubleCourses.append(course)
			self.nonRepairedDoubleCourses.remove(matchResult)
			return
		# 都不在的话m 判断课程类型
		if course["courseType"] == "选修":
			# 选修课则从全部课程中查找课程类型
			query = Courses.objects.filter(courseNum=course["courseNum"])
			if len(query) > 0:
				course["creditType"] = query[0].creditType
			else:
				# 没查到的话...根据课程名再试试
				query = Courses.objects.filter(courseName__contains=course["courseName"])
			 	if len(query) > 0:
			 		course["creditType"] = query[0].creditType
			 	else: # 还查不到的话通过学校网站进行查询
			 		courseInfo = self._getCourseInfo("03", course["courseNum"])
			 		if not courseInfo:
			 			courseInfo = self._getCourseInfo("02", course["courseName"])
			 		if courseInfo:
			 			course["creditType"] = courseInfo
			 		else: # 无法完成匹配 放入不确定课程
						self.uncertainCourses.append(course)
						return 
			self.repairedElective.append(course)
		elif course["courseType"] == "必修":
			query = Courses.objects.filter(courseNum=course["courseNum"])
			if self.college == self.profession: #如果必修课程在当前专业查不到且专业名等于学院名 则可能是类似计软国际班的专业
				for x in query:
					result = Professions.objects.filter(id=x.professionId).filter(grade=self.grade).filter(college=self.college)#学院、年级相同,认为是类似计软国际班的专业
					if len(result) > 0:#若年级符合,则认为专业需要更新.并重新进行课程查询
						self.__init__changeProfession()
						self.profession = result[0].profession
						self.programUrl.append(result[0].url)
						self._start(x.professionId)
						raise Exception("更换专业")
			# 不在其他专业的话...归入不确定课程，让使用者自己放位置
			if len(query) > 0:
				course["creditType"] = query[0].creditType
			# else :
			# 	course["creditType"] = ("理" if self.plan["artsStream"] == 0.0 else "文")
			self.uncertainCourses.append(course)
	
	def _querySetToDic(self, querySet):
		'''
			将查询到的课程结果生成字典形式
		'''
		data = {
			"termNum": self._getTermNum(self.grade, querySet.suggestion),
			"courseNum": querySet.courseNum,
			"courseName": querySet.courseName,
			"courseType": querySet.courseType,
			"credit": querySet.credit,
			"creditType": querySet.creditType
		}
		return data

	def _getCourseInfo(self, searchType, keyword):
		'''
			查询课程信息
			@param searchType string
				01 为开课单位 02 为课程名称 03 为课程总号 04 为模糊查询
			@param keyword string 查询的内容
			@return 学分类型 查询结果多个只返回第一个 查询不到返回None
		'''
		url = "http://192.168.2.224/pyfa/kc.asp"
		params = {
			"cxlb": searchType,
			"keyword": keyword
		}
		response = requests.get(url, params=params)

		self._currentHtml = response.content

		html = response.content
		regx = r'<strong>学分类别：</strong></td><td colspan=3>(\S+?)</td>'
		pm = re.search(regx, html)
		if pm:
			return str(pm.group(1))[:3]
		else:
			return None

	def _getTermNum(self, grade, suggestion):
		'''
			通过年级+建议修读学期计算得到学期号 
			如grade=2015, suggestion=4 则返回20162
			@param grade 年级
			@param suggestion 建议修读学期
			@return
		'''
		suggestion -= 1
		year = int(suggestion/2)
		grade += year
		grade = str(grade)
		grade += str(suggestion % 2 + 1)
		return grade

	@staticmethod
	def _inCourseInCourseList(course, courseList, key, key2=None):
		'''
			通过key值
			判断course是否在courseList中
			在则返回courseList中符合的course
			否则返回None
		'''
		for icourse in courseList:
			if str(course[key]) == str(icourse[key]):
				return icourse
			if key2 and str(course[key2]) == str(icourse[key2]):
				return icourse
			# print str(course[key]), str(icourse[key])
		return None
	
	@property
	def finish(self):
		return self._finish

	@property
	def success(self):
		return self._success

	@property
	def errorInfo(self):
		return self._errorInfo

	def _start(self, professionId=None):
		try:
			if professionId == None:
				self._login()
				self._getBasicInfo()
				self._getRelativeUrl()
			self._getRepairedCourses()
			self._getLatestSelectionResult()
			if professionId == None:
				self._getProfessionId()
			else:
				self.professionId = professionId
			self._getPlan()
			self._getCourses()
			self._retakeCourses()
			self._matchAllCourses()
		except Exception as e:
			if e.message != "更换专业":
				self._errorInfo = e.message
				self._success = False
				self._finish = True

				exstr = traceback.format_exc()
				print exstr
				# 保存错误时的页面信息
				file(os.path.join(DEBUG_DIR, self.stuNum + self._errorInfo + ".txt"), "wb").write(exstr + "\n" + self._currentHtml)
			return
		
		self._success = True
		self._finish = True