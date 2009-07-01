from django.contrib.gis.db import models
from django.db import models as dbmodels
from django.utils import simplejson
from nomenclador.settings import DEFAULT_SRID
from tagging.fields import TagField
import mptt


class MaapModel(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    creator = models.CharField(max_length=20, blank= True) #XXX FIXME Should be a relation to users, should be autoset at creation
    editor = models.CharField(max_length=20, blank= True) #XXX FIXME Should be a relation to users, should be autoset at edition
    tags = TagField()
    category = models.ManyToManyField('MaapCategory', null=True, blank=True, related_name='maapmodel_set')
    objects = models.GeoManager()
            
    class Meta:
        ordering = ('created', 'name',)

    def __unicode__(self):
        return self.name
        
    def getBoxExtent(self):
        """ Need to be defined by particular model """
        pass
#        points = self.point_set.all()  
#        if points:
#            extent = points[0].point
#            for i in range(1,len(points)):
#                extent = extent.union(points[i].point)
#            return extent.extent
    
    @property
    def json_dict(self):
        out = dict.copy(self.__dict__)
        out['box_size'] = self.getBoxExtent()
        out['created'] = self.created.strftime('%D %T')        
        out['changed'] = self.changed.strftime('%D %T')	        

        return out

class MaapCategory(models.Model):
    name = models.CharField(max_length=35)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')    
    maapmodel = models.ManyToManyField(MaapModel, null=True, blank=True, related_name='category_set')

    def __unicode__(self):
        return self.name

    def delete(self):
        super(LayerCategory, self).delete()

class MaapPoint(MaapModel):

    point = models.PointField(srid=DEFAULT_SRID)
    icon = models.ForeignKey('Icon')
    
    def getBoxExtent(self):
        return self.point.extent
    
    @property
    def json_dict(self):
        out = super(MaapPoint, self).json_dict
        out.pop('point')
        out['type'] = 'point'
        out['icon'] = self.icon.json_dict
        out['geojson'] = simplejson.loads(self.point.geojson)
       
        return out
   
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
        
mptt.register(MaapCategory)

