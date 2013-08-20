import re
from urllib2 import urlopen

def get_html(url, code='utf-8'):
    html = urlopen(url).read().decode(code)
    return html


def find_content_between_two_tags(left_tag, right_tag,
                                  text, to_search=r'.*?'):
    reg = left_tag + r'(?P<content>' + to_search + r')' + right_tag
    match = re.search(reg, text)
    if not match:
        raise Exception('can not match: '+reg)
    return match.group('content')


def delete(to_delete, text):
    return re.sub(to_delete, '', text)

