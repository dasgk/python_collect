from django.urls.conf import *
from mysite.controllers.testcontroller import test
from mysite.controllers.timecontroller import show_time
from mysite.controllers.timecontroller import show_time_n
from mysite.controllers.templatecontroller import show_template

urlpatterns = [
    path('test/', test),
    path('show_time/', show_time),
    re_path(r'show_time/([0-9]{4})', show_time_n),
    path('show_template', show_template)
]
