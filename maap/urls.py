from django.conf.urls.defaults import *
import views
import os
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

media_root = os.path.join(os.path.dirname(__file__), 'media')

urlpatterns = patterns('maap.views',
    (r'^$','index'),
    #(r'^markerlayer/(?P<markerlayer_id>\d+)/$', 'marker_layer'),
    (r'^json/object/(?P<object_id>\d+)/$', 'json_object'),
    (r'parques', 'park_list'),
    (r'^parque/(?P<park_id>\d+)/$', 'park_detail'),
    (r'^tags/(?P<tag>[^/]+)/$','obj_list_by_tag'),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root, 'show_indexes':True}),
)
