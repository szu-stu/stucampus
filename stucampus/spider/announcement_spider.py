import re
from django.db import IntegrityError

from stucampus.spider.spider import get_html, delete,\
                                    find_content_between_two_tags
from stucampus.spider.models import Announcement
from to_file import clear_file, write_dic_to_txt


def get_announcement():
    clear_file()
    html = get_html('http://www.szu.edu.cn/board/', 'gb2312')
    needed_text_pattern = (
        r'<td align="center">\d+</td>'
        r'[\s\S]*?'
        r'<td align="center" style="font-size: 9pt">'
        r'\d{4}-\d{1,2}-\d{1,2}'
        r'</td>'
        )
    needed_text_list = re.findall(needed_text_pattern, html)

    already_exist = 0
    print len(needed_text_list)
    for msg_mixed_with_tags in needed_text_list:
        print '1'
        attrs = text_to_dictionary(msg_mixed_with_tags)
        # TODO: replace get_or_create with a url_id checker
        announcement, created = Announcement.objects.get_or_create(
                                    url_id=attrs['url_id'],
                                    title=attrs['title'],
                                    publisher=attrs['publisher'],
                                    category=attrs['category'],
                                    published_date=attrs['date'])
        try:
            announcement.save()
        except IntegrityError:
            already_exist += 1
            
    return already_exist


def text_to_dictionary(text):
    attrs = {}

    left_tag, right_tag = (r'class=fontcolor3>', r'</a></td>')
    title = find_content_between_two_tags(left_tag, right_tag, text)
    to_delete = (r'<font color=black>', r'</font>', r'<b>', r'</b>')
    for pattern in to_delete:
        title = delete(pattern, title)
    attrs['title'] = title[1:] #delete the prefix point 

    left_tag, right_tag = (r'<td align="center" style="font-size: 9pt">',
                           r'</td>')
    attrs['date'] = find_content_between_two_tags(left_tag, right_tag, text,
                                                  r'\d{4}-\d{1,2}-\d{1,2}')

    patterns = {
        'category': (r'<td align="center" style="font-size: 9pt">', r'</td>'),
        'url_id': (r'<a href="view.asp\?id=', r'"'),
        'publisher': (r"document.fsearch1.keyword.value='", r"'"),
        }
    for attr, pattern in patterns.iteritems():
        left_tag, right_tag = pattern
        attrs[attr] = find_content_between_two_tags(left_tag, right_tag, text)

    return attrs


def get_announcement_content(url_id):
    url = 'http://www.szu.edu.cn/board/view.asp?id=' + url_id
    html = get_html(url, 'gb2312')
    left_tag = (r'<td align=center height=30 style="font-size: 9pt">'
                r'<font color=#808080>')
    right_tag = (r'<td height="50" align="right"><table border="0" ce'
                 r'llpadding="0" cellspacing="0" width="90%">')
    text_mixed_with_tags = find_content_between_two_tags(left_tag, right_tag,
                                                         html, r'[\s\S]+?')
    row_text = delete(r'<.+?>', text_mixed_with_tags)
    row_text = delete('\r', row_text)
    row_text = delete(r'&nbsp;', row_text)
    row_text = re.sub('\n+', '\n',  row_text)
    return row_text


if __name__ == '__main__':
    get_main_content('261911')
