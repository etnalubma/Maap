from django.contrib.gis import admin
from models import *
admin.site.register(Icon, admin.GeoModelAdmin)
admin.site.register(MaapPoint, admin.GeoModelAdmin)
admin.site.register(MaapCategory, admin.GeoModelAdmin)

