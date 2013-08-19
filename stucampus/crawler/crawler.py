import re
from urllib.request import urlopen

from stucampus.crawler import Announcement


def get_Announcement():
    html = get_html('http://www.szu.edu.cn/board/', 'gb2312')
    needed_text_pattern = (
        r'<td align="center">\d+</td>'
        r'[\s\S]*?'
        r'<td align="center" style="font-size: 9pt">'
        r'\d{4}-\d{1,2}-\d{1,2}'
        r'</td>'
        )
    needed_text_list = re.findall(needed_text_pattern, html)
    for msg_mixed_with_tags in needed_text_list:
        announcement = text_to_announcement(msg_mixed_with_tags)
        announcement.save()


def get_html(url, code='utf-8'):
    with urlopen(url) as htmlfile:
        html = htmlfile.read().decode(code)
    return html


def text_to_announcement(text):
    left_tag, right_tag = (r'class=fontcolor3>', r'</a></td>')
    title = find_content_between_two_tags(left_tag, right_tag, text)
    to_delete = (r'<font color=black>', r'</font>', r'<b>', r'</b>')
    for pattern in to_delete:
        title = delete(pattern, title)
    title = title[1:] #delete the point prefix

    left_tag, right_tag = (r"document.fsearch1.keyword.value='", r"'")
    publisher = find_content_between_two_tags(left_tag, right_tag, text)

    left_tag, right_tag = (
    return Announcement(title, publisher, category, url_id, date)



def find_content_between_two_tags(left_tag, right_tag,
                                  text, to_search=r'.*?'):
    reg = left_tag + r'?P<content>' + to_search + ')' + right_tag
    match = re.search(reg, text)
    if not match:
        raise Exception('can not match')
    return match.group('content')


def delete(to_delete, text):
    return re.sub(to_search, '', text)
