import json
import urllib2

from django.http import HttpResponse


def render_json(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


def spec_json(status='Error', messages=None):
    if not messages:
        messages = []
    elif not isinstance(messages, (list, tuple)):
        messages = [messages]
    data = {'status': status, 'messages': messages}
    return render_json(data)


def get_client_ip(request):
    '''Get the ip of client'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_http_data(request):
    '''Get form data, used by PUT and DELETE method.'''
    raw_data = request.read()
    data = raw_data.split('&')
    output_dic = {}
    for datum in data:
        d = datum.split('=')
        d_name = d[0]
        d_val = urllib2.unquote(d[1])
        output_dic.update({d_name: d_val})
    return output_dic
