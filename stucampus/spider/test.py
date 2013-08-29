#-*- coding: utf-8 -*-
from spider import get_html, get_etree
import lxml.html


def get_announcement_content(url_id):
    url = 'http://www.szu.edu.cn/board/view.asp?id=' + url_id
    html = get_html(url, code='gbk')
    etree = get_etree(html)

    element_contain_content = etree.xpath('/html/body/table/tr[2]/td/table/'
                                          'tr[3]/td/table/tr[2]/td/table/tr[3]'
                                          )[0]
    content = ''.join(element_contain_content.xpath('td//text()'))
    return content 
                                          

if __name__ == '__main__':
    url_id = '264150'
    print get_announcement_content(url_id)
    '''
    url = 'http://www.szu.edu.cn/board/'
    html = get_html(url, code='gbk')
    etree = lxml.html.fromstring(html)
    path = ('/html/body/table/tr[2]/td/table/tr[3]/td/table'
            '/tr[3]/td/table/tr[position()>2]')
    e_list = etree.xpath(path)

    num = 1
    for e in e_list:
        category = e.xpath('td[2]/text()')[0]
        publisher = e.xpath('td[3]/a/text()')[0]
        date = e.xpath('td[6]/text()')[0]
        title = ''.join(e.xpath('td[4]/*//text()'))
        # |置顶|·
        if u'|置顶|' in title:
            is_stikcy = True
            title = title[4:]
        else:
            is_stikcy = False
        title = title[1:]

        url_id = e.xpath('td[4]/a/@href')[0][12:]
        print url_id
        num += 1
    '''
