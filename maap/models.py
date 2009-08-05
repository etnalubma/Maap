from django.contrib.gis.db import models
from django.db import models as dbmodels
from django.utils import simplejson
from django.contrib.auth.models import User
from osm.models import Nodes
from nomenclador.settings import DEFAULT_SRID
from tagging.fields import TagField
import mptt


class MaapModel(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    creator = models.ForeignKey('auth.User', related_name='creators',editable = False) 
    editor = models.ForeignKey('auth.User',related_name='editors', editable = False)
    tags = TagField()
    category = models.ManyToManyField('MaapCategory', null=True, blank=True, related_name='maapmodel_set')
    objects = models.GeoManager()
            
    class Meta:
        ordering = ('created', 'name',)

    def __unicode__(self):
        return self.name
  
    @property
    def json_dict(self):
        out = dict.copy(self.__dict__)
        out['created'] = self.created.strftime('%D %T')        
        out['changed'] = self.changed.strftime('%D %T')	        

        return out

class MaapCategory(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=35)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')    
    maapmodel = models.ManyToManyField(MaapModel, null=True, blank=True, related_name='category_set')

    def __unicode__(self):
        return self.name

    def delete(self):
        super(LayerCategory, self).delete()

    def get_absolute_url(self):
        return '/maap/category/%s/'%self.slug

class MaapPoint(MaapModel):

    geom = models.PointField(srid=DEFAULT_SRID)
    icon = models.ForeignKey('Icon')
    
    @property
    def json_dict(self):
        out = super(MaapPoint, self).json_dict
        out.pop('geom')
        out['type'] = 'point'
        out['icon'] = self.icon.json_dict
        out['geojson'] = simplejson.loads(self.geom.geojson)
       
        return out

class MaapArea(MaapModel):
    geom = models.PolygonField(srid=DEFAULT_SRID)
   
    @property
    def json_dict(self):
        out = super(MaapArea, self).json_dict
        out.pop('geom')
        out['type'] = 'area'
        out['geojson'] = simplejson.loads(self.geom.geojson)
       
        return out

class MaapOSMArea(MaapArea):
    nodes_covered = models.ManyToManyField('osm.Nodes', editable=False)

    def save(self, force_insert=False, force_update=False):
        super(MaapOSMArea, self).save(force_insert, force_update)
        self.nodes_covered = Nodes.objects.filter(geom__coveredby= self.geom)


class MaapMultiLine(MaapModel):
    geom = models.MultiLineStringField(srid=DEFAULT_SRID)

    @property
    def json_dict(self):
        out = super(MaapMultiLine, self).json_dict
        out.pop('geom')
        out['type'] = 'multiline'
        out['geojson'] = simplejson.loads(self.geom.geojson)

        return out
        
class Icon(models.Model):
    name = models.CharField(max_length=100 )
    image = models.ImageField(upload_to="icons" )

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

