from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from frontend import views as frontend_views


admin.autodiscover()

urlpatterns = patterns('',
                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^$', frontend_views.HomeView.as_view(), name='home'),
                       url(r'^servers/(?P<page>[0-9]+)?$', frontend_views.ServerListView.as_view(), name='servers'),
                       url(r'^server/(?P<pk>\d+)/$', frontend_views.ServerDetailView.as_view(), name='server'),
                       url(r'^server/vote/(?P<pk>\d+)/$', frontend_views.ServerVoteView.as_view(), name='vote'),
                       url(r'^server/review/(?P<pk>\d+)/$', login_required(frontend_views.ReviewCreateView.as_view()),
                           name='review_server'),
                       url(r'^server/banner/(?P<pk>\d+)/$', 'frontend.views.dynamic_banner', name='dynamic_banner'),
                       url(r'^category/(?P<pk>[a-zA-Z0-9\-_]+)/(?P<page>[0-9]+)?$',
                           frontend_views.CategoryDetailView.as_view(), name='category'),
                       url(r'^search/$', frontend_views.SearchView.as_view(), name='search'),

                       # News
                       url(r'^news/$', frontend_views.NewsListView.as_view(), name='news'),
                       url(r'^news/(?P<pk>\d+)/$', frontend_views.NewsDetailView.as_view(), name='news_detail'),

                       # User & Server Control Panel
                       url(r'^servercp/', include('servercp.urls', namespace='servercp')),
                       url(r'^usercp/', include('usercp.urls', namespace='usercp')),

                       # Media file serve path
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),
                       )