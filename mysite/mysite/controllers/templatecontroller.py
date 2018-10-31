from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from datetime import  datetime
def show_template(request):
    return render_to_response('test.html', {'item': '哈哈'})

