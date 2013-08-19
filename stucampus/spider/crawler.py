import re
from urllib2 import urlopen

#from stucampus.spider.models import Announcement


def get_Announcement():
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
    for msg_mixed_with_tags in needed_text_list:
        attrs = text_to_dictionary(msg_mixed_with_tags)
        write_to_txt(attrs)
        #announcement = Announcement(attrs[title], attrs[publisher],
        #                            attrs[category], attrs[url_id, date])
        #announcement.save()


def get_html(url, code='utf-8'):
    #with urlopen(url) as htmlfile:
    #    html = htmlfile.read().decode(code)
    html = urlopen(url).read().decode(code)
    return html


def text_to_dictionary(text):
    attrs = {}
    left_tag, right_tag = (r'class=fontcolor3>', r'</a></td>')
    title = find_content_between_two_tags(left_tag, right_tag, text)
    to_delete = (r'<font color=black>', r'</font>', r'<b>', r'</b>')
    for pattern in to_delete:
        title = delete(pattern, title)
    attrs['title'] = title[1:] #delete the prefix point 

    patterns = {
        'publisher': (r"document.fsearch1.keyword.value='", r"'"),
        'category': (r'<td align="center" style="font-size: 9pt">', r'</td>'),
        'url_id': (r'<a href="view.asp\?id=', r'"')
        }
    for attr, pattern in patterns.iteritems():
        left_tag, right_tag = pattern
        attrs[attr] = find_content_between_two_tags(left_tag, right_tag, text)

    left_tag, right_tag = (r'<td align="center" style="font-size: 9pt">',
                           r'</td>')
    attrs['date'] = find_content_between_two_tags(left_tag, right_tag, text,
                                                  r'\d{4}-\d{1,2}-\d{1,2}')
    return attrs


def find_content_between_two_tags(left_tag, right_tag,
                                  text, to_search=r'.*?'):
    reg = left_tag + r'(?P<content>' + to_search + r')' + right_tag
    match = re.search(reg, text)
    if not match:
        raise Exception('can not match: '+reg)
    return match.group('content')


def delete(to_delete, text):
    return re.sub(to_delete, '', text)


def write_to_txt(dic):
    with open('test.txt', 'a') as f:
        for key, val in dic.iteritems():
            f.write((key+': '+val+'\n').encode('utf-8'))
        f.write('\n')

def clear_file():
    with open('test.txt','w'):
        pass

if __name__ == '__main__':
    get_Announcement()
