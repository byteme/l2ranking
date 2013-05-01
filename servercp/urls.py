from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from servercp import views as servercp_views

urlpatterns = patterns('',
                       url(r'^$', login_required(servercp_views.ServerListView.as_view()), name='servers'),
                       url(r'^add/$', login_required(servercp_views.ServerAddView.as_view()), name='add'),
                       url(r'^update/(?P<pk>\d+)/$', login_required(servercp_views.ServerUpdateView.as_view()),
                           name='update'),
                       url(r'^delete/(?P<pk>\d+)/$', login_required(servercp_views.ServerDeleteView.as_view()),
                           name='delete'),
                       url(r'^info/(?P<pk>\d+)/$', login_required(servercp_views.ServerInfoView.as_view()),
                           name='info'),
                       )