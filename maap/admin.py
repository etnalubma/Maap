from django.contrib.gis import admin
from models import *


class GeoCordobaAdmin(admin.OSMGeoAdmin):
    default_lat = -3686022.8143382
    default_lon = -7145792.0249884 
    #display_wkt = True
    default_zoom = 12    
    map_width = 800
    map_height = 600

    def save_model(self, request, obj, form, change):

        obj.editor = request.user
        if not change:
            obj.creator = request.user
        obj.save()        

    
admin.site.register(Icon, admin.GeoModelAdmin)
admin.site.register(MaapPoint, GeoCordobaAdmin)
admin.site.register(MaapCategory, admin.GeoModelAdmin)
admin.site.register(MaapOSMArea, GeoCordobaAdmin)
admin.site.register(MaapArea, GeoCordobaAdmin)
admin.site.register(MaapMultiline, GeoCordobaAdmin)
