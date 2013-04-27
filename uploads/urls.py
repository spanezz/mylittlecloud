from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = patterns('uploads.views',
    # Examples:
    url(r'^list$', "list_own", name='uploads_list'),
    url(r'^create/$', login_required(views.AreaCreate.as_view()), name='uploads_create'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(views.AreaUpdate.as_view()), name='uploads_edit'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(views.AreaDelete.as_view()), name='uploads_delete'),
    url(r'^area/(?P<uuid>[^/]+)/$', 'public', name='uploads_public'),
)
