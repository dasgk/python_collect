from django.http import HttpResponse
from django.http import Http404
def show_time(request):
    return HttpResponse("这是没有参数的")

def show_time_n(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    return HttpResponse("这是收到的参数："+str(offset))