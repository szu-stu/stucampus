import os
from hashlib import md5

from django import template

from stucampus.settings import APP_ROOT


register = template.Library()
STYLE_ROOT = os.path.join(APP_ROOT, 'static/styles')
SCRIPT_ROOT = os.path.join(APP_ROOT, 'static/scripts')


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
