from django.contrib.gis import admin
from models import *

admin.site.register(Layer, admin.OSMGeoAdmin)
admin.site.register(Point, admin.OSMGeoAdmin)
admin.site.register(Icon, admin.OSMGeoAdmin)

