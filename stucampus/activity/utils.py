#-*- coding: utf-8 -*-
from datetime import datetime, timedelta


MORNING = u'上午'
AFTERNOON = u'下午'


def Generate_Messages_Table(cls):
    message_table = create_empty_table()
    message_table = fill_in_table(message_table, cls)

    return message_table


def create_empty_table():
    message_table = {}
    message_table['date'] = []
    message_table['morning'] = []
    message_table['afternoon'] = []
    message_table['day_tr'] = []

    now = datetime.now()
    date_of_this_Monday = now - timedelta(days=now.weekday())


    for i in range(0, 7):
        date = date_of_this_Monday + timedelta(days=i)
        message_table['date'].append(date)
        message_table['morning'].append([])
        message_table['afternoon'].append([])
        message_table['day_tr'].append({})
        message_table['day_tr'][i]['date'] = date

        message_table['day_tr'][i]['morning'] = []
        message_table['day_tr'][i]['afternoon'] = []



    return message_table


def fill_in_table(message_table, cls):
    messages_this_week = get_messages_this_week(cls)
    to_be_published = messages_this_week.filter(checked=True)

    for msg in to_be_published:
        if msg.time == MORNING:
            message_table['day_tr'][msg.date.weekday()]['morning'].append(msg)
            message_table['morning'][msg.date.weekday()].append(msg)
        else:
            message_table['day_tr'][msg.date.weekday()]['afternoon'].append(msg)
            message_table['afternoon'][msg.date.weekday()].append(msg)


    return message_table


def get_messages_this_week(cls):
    now = datetime.now()
    date_of_this_Monday = now - timedelta(days=now.weekday())
    date_of_next_Monday = date_of_this_Monday + timedelta(days=7)
    lecture_held_this_week = cls.objects.filter(
        date__gte=date_of_this_Monday,
        date__lt=date_of_next_Monday)

    return lecture_held_this_week
