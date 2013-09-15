import urllib2


class PutHTTPMethodDataMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == 'PUT':
            raw_data = request.read()
            data = raw_data.split('&')
            put_data = {}
            for datum in data:
                data_name, data_value = datum.split('=', 1)
                data_value = urllib2.unquote(data_value)
                put_data.update({data_name: data_value})
            request.PUT = put_data
        return None
