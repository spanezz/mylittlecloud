from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^license/$', TemplateView.as_view(template_name='license.html'), name='license'),
    url(r'^uploads/', include('uploads.urls')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {
        #'next': reverse_lazy('home'),
    }, name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {
        'next_page': reverse_lazy('home'),
    }, name="logout"),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
