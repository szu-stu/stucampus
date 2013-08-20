# run to get all publisher(about 100), not run by django
import re

from spider import get_html, find_content_between_two_tags
from to_file import add_line_to_file, clear_file


def get_publisher():
    clear_file()
    html = get_html('http://www.szu.edu.cn/board/userlist.asp', 'gb2312')
    needed_text_pattern = r'>\d+.*?</option>'
    all_needed_list = re.findall(needed_text_pattern, html)
    if not all_needed_list:
        raise Exception('can not find')
    left_tag, right_tag = (r'>\d+', r'</option>')
    publisher_list = []
    for msg_mixed_with_tags in all_needed_list:
        row_text = find_content_between_two_tags(left_tag, right_tag,
                                                 msg_mixed_with_tags)
        row_text = row_text[1:] # delete the prefix point
        publisher_list.append(row_text)
    return publisher_list

def create_choice_for_model(publisher_list):
    filename = 'data_for_models.py'
    clear_file(filename)
    add_line_to_file(filename, u'#-*- coding: utf-8')
    add_line_to_file(filename, u'#produced by publiser_spider.py')
    add_line_to_file(filename, u'PUBLISHER_CHOICES = (')
    for p in publisher_list:
        add_line_to_file(filename, u"    ('%s', '%s'),"%(p,p))
    add_line_to_file(filename, u')')


if __name__ == '__main__':
    publisher_list = get_publisher()
    create_choice_for_model(publisher_list)
