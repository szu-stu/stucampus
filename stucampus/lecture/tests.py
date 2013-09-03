# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import date, time
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
import datetime

from stucampus.spider.models import Announcement
from stucampus.lecture.models import LectureMessage
from stucampus.lecture.implementation import get_title, get_speaker
from stucampus.lecture.implementation import get_place, get_time, get_date
from stucampus.lecture.implementation import get_datetime
from stucampus.lecture.implementation import search_lecture_announcement

class ParseTest(TestCase):
    def test_parse(self):
        url_id_all = ('264016', '260145', '259928', '258344', '257332', '256927', '256700', '258106')
        num_of_update = Announcement.fetch_new_announcement(30)
        self.assertEqual(num_of_update>0, True)
        print num_of_update

        academic_ancmts = Announcement.objects.filter(category=u'学术')
        lecture_ancmts = search_lecture_announcement(academic_ancmts)
        #lecture_ancmts = []
        #for url_id in url_id_all:
        #    try:
        #        la = Announcement.objects.get(url_id=url_id)
        #    except ObjectDoesNotExist:
        #        continue
        #    lecture_ancmts.append(la)
        content_list = [ (ancmt.get_content(), ancmt.url_id)\
                        for ancmt in lecture_ancmts ]
        self.assertEqual(len(content_list)>0, True)


        for content, url_id in content_list:
            print '----------- message -------------'
            print url_id
            title = get_title(content)
            print title
            #self.assertEqual(len(title)>3, True)
            speaker = get_speaker(content)
            print speaker
            #self.assertEqual(len(speaker)>1,  True)
            place = get_place(content)
            print place
            #self.assertEqual(len(place)>2, True)
            datetime = get_datetime(content)
            print datetime

