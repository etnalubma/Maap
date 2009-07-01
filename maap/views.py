from django.shortcuts import render_to_response
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from models import MaapModel, MaapPoint, Icon, MaapCategory
from django.views.generic.list_detail import object_list, object_detail
from tagging.models import TaggedItem, Tag

def convOSM(wkt):
    """ Converts standard merkartor 
        to osm projection as tuple 
    """
    obj = OGRGeometry(wkt)
    obj.srs = 'EPSG:4326'
    obj.transform_to(SpatialReference('EPSG:900913'))
    #obj.transform_to(SpatialReference('EPSG:4326'))
    return (obj.x, obj.y)

def obj_list_by_cat(request, cat_slug):
    try:
        catel = MaapCategory.objects.get(slug = cat_slug)
    except MaapCategory.DoesNotExist:
        raise Http404
    qscats = catel.get_descendants(include_self=True)
    mmodels = MaapModel.objects.filter(category__in=qscats)
    context = RequestContext(request, {'category':catel, 'objects':mmodels})
    return render_to_response('maap/list_by_cat.html', context_instance=context)
    
    
def obj_list_by_tag(request, tag):
    tagins = Tag.objects.get(name=tag)
    context = RequestContext(request, {'tag':tagins})
    return render_to_response('maap/list_by_tag.html', context_instance=context)

def maap_object_detail(request,cat_slug, object_id):
    objects = MaapModel.objects.all()
    return object_detail(request, objects, int(object_id), 
                         template_name='maap/object_detail.html')

    
def park_list(request):
    parks = MaapModel.objects.filter(tags__contains ='park')
    #TaggedItem.objects.get_by_model(MaapModel,'park')
    return object_list(request, parks, template_name='maap/park_list.html')
    
def json_object(request, object_id):
    try:
        mobject = MaapModel.objects.get(pk=int(object_id))
    except MaapModel.DoesNotExist:
        raise Http404
    point = mobject.maappoint
    layer = {
        'type': 'layer',
        'id': 'layer-object-%s' % object_id,
        'elements': [point.json_dict],
        'box_size': point.getBoxExtent()
    }
    return HttpResponse(simplejson.dumps(layer), mimetype='text/json')

def index(request):
   
    mls = MaapModel.objects.all()
   
      
    mls = MaapModel.objects.all()
    context = RequestContext(request, {'layer_list':mls})
    return render_to_response('index.html', context_instance=context )    
    

