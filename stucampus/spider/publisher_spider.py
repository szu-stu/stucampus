# run to get all publisher(about 100), not run by django
from annoucement_spider import get_html, delete, write_to_txt, clear_file,\
                               find_content_between_two_tags


def get_publisher():
    print 'test'
    clear_file()
    html = get_html('http://www.szu.edu.cn/board/userlist.asp', 'gb2312')
    with open('test.txt','w') as f:
        f.write(html.encode('utf-8'))


if __name__ == '__main__':
    get_publisher()
