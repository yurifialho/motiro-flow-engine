from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.assessment import views


urlpatterns = [
    url(r'^criteria/(?P<pk>[0-9]+)/$', views.criteria_detail),
    url(r'^criteria/$', views.criteria_list),
    url(r'^quiz/(?P<pk>[0-9]+)/$', views.quiz_detail),
    url(r'^quiz/$', views.quiz_list),
    url(r'^answer/(?P<pk>[0-9]+)/$', views.quiz_detail),
    url(r'^answer/$', views.quiz_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
