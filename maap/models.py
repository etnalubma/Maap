from django.contrib.gis.db import models
from django.db import models as dbmodels
from django.utils import simplejson
from nomenclador.settings import DEFAULT_SRID
from tagging.fields import TagField

class Layer(models.Model):
    name = models.CharField(max_length=35)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    creator = models.CharField(max_length=20, blank= True)
    editor = models.CharField(max_length=20, blank= True)
    description = models.TextField(blank=True)
    tags = TagField()

    objects = models.GeoManager()

    class Meta:
        ordering = ('created', 'name',)

    def __unicode__(self):
        return self.name
        
    def getBoxExtent(self):
        points = self.point_set.all()  
        if points:
            extent = points[0].point
            for i in range(1,len(points)):
                extent = extent.union(points[i].point)
            return extent.extent
        
        
    
    @property
    def json_dict(self):
        out = dict.copy(self.__dict__)
        out['box_size'] = self.getBoxExtent()
        out['created'] = self.created.strftime('%D %T')        
        out['changed'] = self.changed.strftime('%D %T')	        
        out['type'] = 'layer'
        out['elements'] = [p.json_dict for p in self.point_set.all()]      
        return out

#class PointsLayer(Layer):
#    name = models.CharField(max_length=35)
#    objects = models.GeoManager()

class Point(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField(blank=True)
    point = models.PointField(srid=DEFAULT_SRID)
    icon = models.ForeignKey('Icon')
    layer = models.ForeignKey('Layer')
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    creator = models.CharField(max_length=20, blank= True)
    editor = models.CharField(max_length=20, blank= True)

    objects = models.GeoManager()

    class Meta:
        ordering = ('created', 'name',)

    def __unicode__(self):
        return self.name
    
    @property
    def json_dict(self):
        out = dict.copy(self.__dict__)
        out.pop('point')
        out['type'] = 'point'
        out['icon'] = self.icon.json_dict
        out['geojson'] = simplejson.loads(self.point.geojson)
        out['created'] = self.created.strftime('%D %T')        
        out['changed'] = self.changed.strftime('%D %T')	        
        
        return out

class Photo(models.Model):
    image = models.ImageField(upload_to='images', blank= True)
    def __unicode__(self):
        return "IMG%i" %self.pk
    
class Icon(models.Model):
    name = models.CharField(max_length=100 )
    image = models.ImageField(upload_to="image" )

    def __unicode__( self ):
        return self.name

    @property
    def json_dict(self):
        out = {}
        out['url'] = self.image.url
        out['width'] = self.image.width
        out['height'] = self.image.height
        return out
