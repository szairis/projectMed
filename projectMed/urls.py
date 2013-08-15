from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Following block is for the maintenance
    #url(r'^$','agora.views.maintenance'),
    #url(r'^$','agora.views.maintenance'),
    #url(r'^agora/$','agora.views.mainenance'),
    #url(r'^browse/$','agora.views.maintenance'),
    #url(r'^search_listings/$','agora.views.maintenance'),
    #url(r'^listings/(?P<encrypted_id>.*?)L/$','agora.views.maintenance'),
    #url(r'^modify_listing/(?P<encrypted_id>.*?)L/$','agora.views.maintenance'),
    #url(r'^edit_project/(?P<encrypted_id>.*?)L/$','agora.views.maintenance'),
    #url(r'^submit/$','agora.views.post_project'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #url(r'^$','agora.views.coming_soon'),
    url(r'^coming_soon/$','agora.views.coming_soon'),
    url(r'^$','agora.views.index'),
    url(r'^agora/$','agora.views.index'),
    url(r'^browse/$','agora.views.listings'),
    url(r'^search_listings/$','agora.views.search_listings'),
    url(r'^listings/(?P<encrypted_id>.*?)L/$','agora.views.detail'),
    url(r'^modify_listing/(?P<encrypted_id>.*?)L/$','agora.views.mod_list'),
    url(r'^edit_project/(?P<encrypted_id>.*?)L/$','agora.views.edit_project'),
    url(r'^submit/$','agora.views.post_project'),
    url(r'^about/$','agora.views.about'),
    url(r'^contact/$','agora.views.contact'),
    url(r'^terms/$','agora.views.terms'),
    url(r'^maintenance/$','agora.views.maintenance'),

    url(r'^submit_success/$','agora.views.submission_success'),
    url(r'^reply_success/$','agora.views.reply_success'),
    url(r'^delete_success/$','agora.views.delete_success'),
    url(r'^edit_success/$','agora.views.edit_success'),
    url(r'^sorry/$','agora.views.one_per_minute'),

    url(r'^blog/$','blog.views.blog_posts'),
    url(r'^blog/(?P<blog_post_slug>.*?)/$','blog.views.detail'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
