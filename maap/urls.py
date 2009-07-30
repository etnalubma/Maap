from django.conf.urls.defaults import *
import views
import os
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

media_root = os.path.join(os.path.dirname(__file__), 'media')

urlpatterns = patterns('maap.views',
    (r'^$','index'),
    (r'^api/get$', 'get_objects'),
#    (r'^json/object/(?P<object_id>\d+)/$', 'json_object'),
    (r'^category/(?P<cat_slug>[^/]+)/$', 'obj_list_by_cat'),
    (r'^streets/$', 'search_streets'),
    (r'^streets/location$', 'street_location'),
    (r'(?P<cat_slug>[^/]+)/(?P<object_id>\d+)/$','maap_object_detail'),
    (r'^tags/(?P<tag>[^/]+)/$','obj_list_by_tag'),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root, 'show_indexes':True}),
)
