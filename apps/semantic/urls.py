from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.semantic import views

urlpatterns = [
    url(r'^query/$', views.query_sparql),
    url(r'^classes/$', views.get_all_owl_classes),
    url(r'^instances/$', views.get_all_owl_instances),
    url(r'^sync/$', views.sync),
    url(r'^force_delete/$', views.force_delete),
]

urlpatterns = format_suffix_patterns(urlpatterns)
