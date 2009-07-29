from django.shortcuts import render_to_response
from django.db import connection
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from osm.models import *
from models import MaapModel, MaapPoint, Icon, MaapCategory

from tagging.models import TaggedItem, Tag

from osm.utils import get_locations_by_intersection, get_location_by_door

def get_streets_list(street):
    """ Esta funcion auxiliar sirve para desambiguar una busqueda de calles y matar gatitos. """

    cursor = connection.cursor()

    cursor.execute("""SELECT DISTINCT osm_searchableway.name FROM osm_searchableway WHERE osm_searchableway.name ILIKE %s""",['%%%s%%' % street])
    return cursor.fetchall()    



def street_lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if u'query' in request.GET:
            value = request.GET[u'query']
            # puto el que lee
            if len(value) > 2:
                model_results = get_streets_list(value)
                
                
                results = [ x[0] for x in model_results ]
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def search_streets(request):
    if request.method == 'GET':
        pass
    else :
        pass

    context = RequestContext(request,{'results':''})

    
    return render_to_response('maap/streets.html', context_instance=context)


def get_streets_json(request):
    #return point_intersection(request, 'Independencia', 200)
    results = get_locations_by_intersection('9 de Julio','Rivera Indarte')    
    
    points = []
    for r in results:

        pgeom = OGRGeometry(r.wkt)
        pgeom.srs = 'EPSG:4326'
        pgeom.transform_to(SpatialReference('EPSG:900913'))
        pcoord = simplejson.loads(pgeom.json)
        points.append({
          "type": "point",
          "id": '23', 
          "name": "pipin",
          "geojson": pcoord, 
          "icon": {
            "url": "/media/icons/soccer.png", 
            "width": 32, 
            "height": 37
            }
        })
  
    layer = {
        'type': 'layer',
        'id': 'layer-object-%s' % 'layer',
        'elements': points,
        'box_size': None
    }
    return HttpResponse(simplejson.dumps(layer), mimetype='text/json')    
    



def point_intersection(request, string, door):
    res = get_location_by_door(string, door)
    if not res:
        raise Http404

    # cast geometry data and change projection from way polygon
    resgeom = OGRGeometry(res[0].wkt)
    resgeom.srs = 'EPSG:4326'
    resgeom.transform_to(SpatialReference('EPSG:900913'))

    # Get ways data
    qset = WayNodes.objects.select_related('way_searchableway', 'node').filter(way__searchableway__name__startswith = string)    
    # Set points grouped by way
    waysdict = {}
    for wn in qset:
        try:
            # This is making queries, need to be checked
            door = wn.waynodesdoor.number
        except WayNodesDoor.DoesNotExist:
            door = None
        point = {
            'way_id': wn.way_id,
            'geom': wn.node.geom,
            'door':door,
            'id': wn.node.id,
        }
        if wn.way_id in waysdict.keys():
            waysdict[wn.way_id].append(point)
        else:
            waysdict[wn.way_id] = [point]
    
    # get all nodes from ways result and append as a maap.point json
    nodes = reduce(lambda x,y: x+y, waysdict.values(), [])    
    nodes = filter(lambda n: n['door'] is not None, nodes)
    points = []
    for p in nodes: 
        pgeom = OGRGeometry(p['geom'].wkt)
        pgeom.srs = 'EPSG:4326'
        pgeom.transform_to(SpatialReference('EPSG:900913'))
        pcoord = simplejson.loads(pgeom.json)
        points.append({
          "type": "point",
          "id": p['id'], 
          "name": "pipin",
          "geojson": pcoord, 
          "icon": {
            "url": "/media/icons/soccer.png", 
            "width": 32, 
            "height": 37
            }
        })
    
    points.append({
      "type": "point",
      "id": 'result', 
      "name": "result",
      "geojson": simplejson.loads(resgeom.json), 
      "icon": {
        "url": "/media/icons/info.png", 
        "width": 32, 
        "height": 37
        }
    })
    
    layer = {
        'type': 'layer',
        'id': 'layer-object-%s' % 'layer',
        'elements': points,
        'box_size': None
    }
    return HttpResponse(simplejson.dumps(layer), mimetype='text/json')


def get_objects(request):

    if request.method == 'GET':
        params = request.GET        
        

        qset = MaapModel.objects.all()

        if params.has_key('id'):
            qset &= MaapModel.objects.filter(pk = int(params['id']))

        if params.has_key('searchterm'):
            qset&= MaapModel.objects.filter(name__icontains=params['searchterm'])

        if params.has_key('category'):
            try:
                catel = MaapCategory.objects.get(slug = params['category'])
            except MaapCategory.DoesNotExist:
                raise Http404
            qscats = catel.get_descendants(include_self=True)
            qset = qset.filter(category__in=qscats)
            
        if params.has_key('tag'):
            qset &= TaggedItem.objects.get_by_model(MaapModel, params['tag'])
        
                
        if params.has_key('out'):
            out = params['out']
            if out == 'layer':
                layer = json_layer(qset)
                return HttpResponse(simplejson.dumps(layer), mimetype='text/json')  
            else:
                raise Http404    
        else:
            path = request.get_full_path() + '&out=layer'
            context = RequestContext(request, {'objs': qset, 'layerpath':path})
            return render_to_response('maap/results.html', context_instance=context)
            
    else:
        raise Http404
        
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
    result = TaggedItem.objects.get_by_model(MaapModel, tag)
    context = RequestContext(request, {'tag':tag , 'objs': result})
    return render_to_response('maap/list_by_tag.html', context_instance=context)

def maap_object_detail(request,cat_slug, object_id):
    objects = MaapModel.objects.all()
    return object_detail(request, objects, int(object_id), 
                         template_name='maap/object_detail.html')

    
def park_list(request):
    parks = MaapModel.objects.filter(tags__contains ='park')
    #TaggedItem.objects.get_by_model(MaapModel,'park')
    return object_list(request, parks, template_name='maap/park_list.html')
    
def json_layer(qset):
    points = [ mo.maappoint for mo in qset]
    if points:
        extent = points[0].point
        for i in range(1,len(points)):
            extent = extent.union(points[i].point)
        box_size = extent.extent    
    else:
        box_size = ''
    
    json_results = [p.json_dict for p in points]
    layer = {
        'type': 'layer',
        'id': 'layer-object-%s' % 'layer',
        'elements': json_results,
        'box_size': box_size
    }
    return layer

def index(request):
   
    mls = MaapModel.objects.all()
   
      
    mls = MaapModel.objects.all()
    context = RequestContext(request, {'layer_list':mls})
    return render_to_response('index.html', context_instance=context )    
    

