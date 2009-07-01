from django.contrib.gis import admin
from models import *
admin.site.register(Icon, admin.OSMGeoAdmin)
admin.site.register(MaapPoint, admin.OSMGeoAdmin)
admin.site.register(MaapCategory, admin.OSMGeoAdmin)

