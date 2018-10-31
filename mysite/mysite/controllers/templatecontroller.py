from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Template,Context
from datetime import  datetime
def show_template(request):
    return render_to_response('test.html', {'person_name':'周建业'})

