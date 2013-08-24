import re
from urllib2 import urlopen


class MatchError(Exception):
    def __init__(self, text, reg):
        self.text = text
        self.reg = reg
    def __str__(self):
        return "can't match " + self.reg.encode('utf-8') + " in:\n"\
               + self.text.encode('utf-8')


def get_html(url, code='utf-8'):
    return urlopen(url).read().decode(code, 'ignore')


def find_content_between_two_tags(left_tag, right_tag,
                                  text, to_search=r'.*?'):
    reg = left_tag + r'(?P<content>' + to_search + r')' + right_tag
    match = re.search(reg, text)
    if not match:
        raise MatchError(text, reg)
    return match.group('content')


def delete(to_delete, text):
    return re.sub(to_delete, '', text)

