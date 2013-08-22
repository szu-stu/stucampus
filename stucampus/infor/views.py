from django.shortcuts import render

from stucampus.infor.models import Infor


def list(request):
    infors = Infor.objects.order_by('created').reverse().all()
    return render(request, 'infor/list.html',
                 {'lastly_infors': infors[:5],
                  'secondly_lastly_infors': infors[5:15]})
