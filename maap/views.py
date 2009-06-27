from django.shortcuts import render_to_response
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from models import Layer, Point, Icon

from django.views.generic.list_detail import object_list, object_detail

from tagging.models import Tag

def obj_list_by_tag(request, tag):
    tagins = Tag.objects.get(name=tag)
    context = RequestContext(request, {'tag':tagins})
    return render_to_response('maap/list_by_tag.html', context_instance=context)


def park_detail(request, park_id):
    parks = Tag.objects.get(name='park')
    return object_detail(request, parks, park_id, template_name='maap/park_detail.html')
    
def park_list(request):
    parks = Tag.objects.get(name='park')
    return object_list(request, parks, template_name='maap/park_list.html')
    
def convOSM(wkt):
    """ Converts standard merkartor 
        to osm projection as tuple 
    """
    obj = OGRGeometry(wkt)
    obj.srs = 'EPSG:4326'
    obj.transform_to(SpatialReference('EPSG:900913'))
    #obj.transform_to(SpatialReference('EPSG:4326'))
    return (obj.x, obj.y)

def layer(request, layer_id):
    try:
        layer = Layer.objects.get(pk=int(layer_id))
    except Layer.DoesNotExist:
        raise Http404
    
    return HttpResponse(simplejson.dumps(layer.json_dict), mimetype='text/json')


def index(request):
   
    mls = Layer.objects.all()
   
    return render_to_response(
        'index.html',
        {
            'layer_list': mls, 
        }
    )
    
    
def marker_layer(request, markerlayer_id):
    mks = Layer.objects.all()[0].point_set.all()
    
    points = [
        {
            'icon':m.icon.image.url,
            'point':m.point.geojson,
        } for m in mks
    ]
    return HttpResponse(simplejson.dumps(points), mimetype='text/json')


