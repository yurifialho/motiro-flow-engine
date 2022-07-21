from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.kipco import views
from apps.bpmn import views as bpmnviews


urlpatterns = [
    url(r'^process/(?P<pk>\b([a-f0-9]{40})\b)/$', views.intensive_process_detail),
    url(r'^process/(?P<pk>\b([a-f0-9]{40})\b)/activities$',
        views.activity_by_process_list),
    url(r'^process/$', views.intensive_process_list),
    url(r'^process/owl/$', bpmnviews.flowelementscontainerowl_list),

    url(r'^processgoal/(?P<pk>\b([a-f0-9]{40})\b)/$', views.processgoal_detail),
    url(r'^processgoal/$', views.processgoal_list),

    url(r'^activity/(?P<pk>\b([a-f0-9]{40})\b)/$', views.activity_detail),
    url(r'^activity/$', views.activity_list),

    url(r'^activitygoal/(?P<pk>\b([a-f0-9]{40})\b)/$', views.activitygoal_detail),
    url(r'^activitygoal/$', views.activitygoal_list),

    url(r'^intention/(?P<pk>\b([a-f0-9]{40})\b)/$', views.intention_detail),
    url(r'^intention/$', views.intention_list),

    url(r'^desire/(?P<pk>\b([a-f0-9]{40})\b)/$', views.desire_detail),
    url(r'^desire/$', views.desire_list),

    url(r'^agenttype/(?P<pk>\b([a-f0-9]{40})\b)/$', views.agenttype_detail),
    url(r'^agenttype/$', views.agenttype_list),

    url(r'^agentspecialty/(?P<pk>\b([a-f0-9]{40})\b)/$', views.agentspecialty_detail),
    url(r'^agentspecialty/$', views.agentspecialty_list),

    url(r'^agent/(?P<pk>\b([a-f0-9]{40})\b)/$', views.agent_detail),
    url(r'^agent/$', views.agent_list),

    url(r'^socialization/(?P<pk>\b([a-f0-9]{40})\b)/$', views.socialization_detail),
    url(r'^socialization/$', views.socialization_list),

    url(r'^document/(?P<pk>\b([a-f0-9]{40})\b)/$', views.document_detail),
    url(r'^document/$', views.document_list),

    url(r'^data_object/(?P<pk>\b([a-f0-9]{40})\b)/$', views.data_object_detail),
    url(r'^data_object/$', views.data_object_list),

    url(r'^attribute/(?P<pk>\b([a-f0-9]{40})\b)/$', views.attribute_detail),
    url(r'^attribute/$', views.attribute_list),

]

urlpatterns = format_suffix_patterns(urlpatterns)
