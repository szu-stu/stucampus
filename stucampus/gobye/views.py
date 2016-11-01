#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .creditStatistics import CreditStatistics

import os
DEBUG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DEBUG")


def login(request):
	error = request.GET.get("error", "")
	(img, cookie) = CreditStatistics.getCaptcha()
	return render(request, 'gobye/login.html', {"cookie":cookie, "img":img, "error":error})

def result(request):
	if request.method == "POST":
		stuNum = request.POST.get("stuNum", "")
		stuPwd = request.POST.get("stuPwd", "")
		captcha = request.POST.get("captcha", "")
		capCookie = request.POST.get("capCookie", "")

		cs = CreditStatistics(stuNum, stuPwd, captcha, capCookie)
		while cs.finish == False:
			time.sleep(1)
		if cs.success:
			plan = cs.plan
			double = cs.minorProfessionId
			minorRemark = plan["minorRemark"]
			doubleRemark = plan["doubleRemark"]
			params = {
				"repairedPublicCourses":cs.repairedPublicCourses, 
				"repairedProfessionCourses":cs.repairedProfessionCourses, 
				"repairedProfessionElective":cs.repairedProfessionElective, 
				"repairedElective":cs.repairedElective, 
				"failCourses":cs.failCourses, 
				"nonRepairedPublicCourses":cs.nonRepairedPublicCourses, 
				"nonRepairedProfessionCourses":cs.nonRepairedProfessionCourses, 
				"optionalCourses":cs.optionalCourses,
				"repairedDoubleCourses": cs.repairedDoubleCourses,
				"nonRepairedDoubleCourses": cs.nonRepairedDoubleCourses,
				"uncertainCourses": cs.uncertainCourses,
				"doubleRemark": doubleRemark,
				"minorRemark": minorRemark,
				"programUrl": cs.programUrl,
				"publicRequired": plan["publicRequired"],
				"professionalElective": plan["professionalElective"],
				"artsStream": plan["artsStream"],
				"scienceStream": plan["scienceStream"],
				"elective": plan["elective"],
				"professionalRequired": plan["professionalRequired"],
				"double": double,
				"profession": cs.profession,
				"college": cs.college
			}
			return render(request, 'gobye/result.html', params)

		(img, cookie) = CreditStatistics.getCaptcha()
		return HttpResponseRedirect("/?error=" + cs.errorInfo)

	# 非POST方法跳转到登录页面
	return HttpResponseRedirect("/")

def feedback(request):
	return render(request, 'gobye/feedback.html')

def feedbackInfo(request):
	if request.method == "POST":
		contact = request.POST.get("contact", "")
		content = request.POST.get("content", "")
		fil = open(os.path.join(DEBUG_DIR, "feedback.txt"), "rw+")
		filecontent = fil.readlines()
		tmpContent = ""
		for tmp in filecontent:
			tmpContent += tmp
		fil.close()
		file(os.path.join(DEBUG_DIR, "feedback.txt"), "wb").write(tmpContent + "\n" + "contact:" + contact + "content:" + content)
		
		return render(request, 'gobye/feedbackInfo.html')
	else :
		return HttpResponseRedirect("/")

		
