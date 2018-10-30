from django.http import HttpResponse
def show_time(request):
    return HttpResponse("这是没有参数的")

def show_time_n(request, offset):
    return HttpResponse("这是收到的参数："+str(offset))