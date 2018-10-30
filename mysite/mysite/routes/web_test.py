from django.urls.conf import *
from mysite.controllers.testcontroller import test
urlpatterns = [
path('admin/', test),
]
