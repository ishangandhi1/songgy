from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'moves_like_django.views.home', name='home'),
    # url(r'^moves_like_django/', include('moves_like_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^harmonify/',include('harmonify.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^$', include('pages.urls')),
)
handler404 = 'harmonify.views.custom_404'
handler400 = 'harmonify.views.custom_404'
handler403 = 'harmonify.views.custom_404'
handler500 = 'harmonify.views.custom_404'