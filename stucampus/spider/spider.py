import re
from urllib2 import urlopen
import lxml.html
import requests

class MatchError(Exception):

    def __init__(self, text='', reg=''):
        self.text = text
        self.reg = reg
        message = "can't match :\n"
        message += self.reg.encode('utf-8')
        message += "\nin:\n"
        message += self.text.encode('utf-8')
        super(MatchError, self).__init__(message)

    def __str__(self):
        return "can't match " + self.reg.encode('utf-8') + " in:\n"\
               + self.text.encode('utf-8')


def fetch_html_by_get(url, encoding=None):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = encoding or response.encoding
    return response.text


def fetch_html_by_post(url, form_data, encoding=None):
    response = requests.post(url, data=form_data)
    response.raise_for_status()
    response.encoding = encoding or response.encoding
    return response.text


def find_content_between_two_marks(left_tag, right_tag,
                                  text, to_search=r'.*?'):
    reg = left_tag + r'(?P<content>' + to_search + r')' + right_tag
    match = re.search(reg, text)
    if not match:
        raise MatchError(text, reg)
    return match.group('content')


def delete(to_delete, text):
    return re.sub(to_delete, '', text)
