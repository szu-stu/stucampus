import os
import re
from hashlib import md5

from django import template

from stucampus.settings import path


register = template.Library()
STYLE_ROOT = path('stucampus', 'static', 'styles')
SCRIPT_ROOT = path('stucampus', 'static', 'scripts')


@register.filter(name='as_css', is_safe=True)
def as_css(path):
    try:
        css = open(os.path.join(STYLE_ROOT, path))
    except:
        ver = ''
    else:
        ver = ('?ver=%s' % md5(css.read()).hexdigest()[0:6])
    html = ('<link rel="stylesheet" href="/static/styles/%s%s"'
            ' type="text/css" />' % (path, ver))
    return html


@register.filter(name='as_js', is_safe=True)
def as_js(path):
    try:
        js = open(os.path.join(SCRIPT_ROOT, path))
    except:
        ver = ''
    else:
        ver = ('?ver=%s' % md5(js.read()).hexdigest()[0:6])
    html = ('<script type="text/javascript"'
            ' src="/static/scripts/%s%s"></script>' % (path, ver))
    return html


class StripspacesNode(template.base.Node):
    def __init__(self, nodelist, replacement=' '):
        self.nodelist = nodelist
        self.replacement = replacement

    def render(self, context):
        return re.sub(r'\s{2,}', self.replacement,
                      (self.nodelist.render(context).strip()))


@register.tag
def nospaces(parser, token):
    nodelist = parser.parse(('endnospaces',))
    parser.delete_first_token()
    return StripspacesNode(nodelist, replacement='')
