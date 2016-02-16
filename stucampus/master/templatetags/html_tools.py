import os
import re
from hashlib import md5

from django import template
from django.conf import settings

from stucampus.settings import path
from ipware.ip import get_real_ip


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


@register.simple_tag(takes_context=True)
def autoSwapCDN( context, filepath ):
    try:
        request = context['request']
        ip =  get_real_ip(request)

        fullpath = settings.STATIC_URL + filepath

        #return cdn address if is public ip
        if ip is not None and hasattr(settings,'QINIU_BUCKET_DOMAIN'):
            # we have a real, public ip address for user
            fullpath = '//' + settings.QINIU_BUCKET_DOMAIN + fullpath
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument" % filepath)
    return fullpath


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    dict_ = context['request'].GET.copy()
    dict_[field] = value
    return '?'+dict_.urlencode()
