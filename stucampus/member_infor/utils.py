#-*- coding: utf-8
import datetime

def getdate(date):
    if date is "":
        return ""
    __s_date = datetime.date(1899, 12, 31).toordinal()-1
    if not isinstance(date, int):
        date = int(date)
    d = datetime.date.fromordinal(__s_date + date)
    return d.strftime("%Y-%m-%d")