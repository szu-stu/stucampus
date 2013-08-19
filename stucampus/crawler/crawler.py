import re
from urllib.request import urlopen


def get_annoucement_list(url, code='utf-8'):
    with urlopen(url) as f:
        html = f.read().decode(code)
    content_list_with_tag = re.findall(r'
