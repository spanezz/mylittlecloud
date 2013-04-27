from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('uploads.views',
    # Examples:
    url(r'^list$', "list_own", name='uploads_list'),
)
