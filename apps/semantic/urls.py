from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.semantic import views

urlpatterns = [
    url(r'^query/$', views.query_sparql),
    url(r'^classes/$', views.get_all_owl_classes),
    url(r'^instances/$', views.get_all_owl_instances),
]

urlpatterns = format_suffix_patterns(urlpatterns)
