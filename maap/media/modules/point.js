//this funcion take a id of layer and add the points contained in the layer to the state variable and return the generated list points or 1 if an error appear. 
/*
function addPointsFromLayerToState(layerid) {
    //send request to server for get the points list to add to map 
    $.getJSON('markerlayer/'+layerid, 
        function(data) {
             //push list points in the state variable
             res = generateMarkersList(data)

             return res
        }
     );
     return 1;
}

//this function show a point in the map. His input depend from the geojson format.  
function showMarker(x,y,layer) {
    //show a marker. For now this function just add a marker to a layer. 
    //marker is a object lonlat
    var size = new OpenLayers.Size(10,17);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var icon = new OpenLayers.Icon('http://boston.openguides.org/markers/AQUA.png',size,offset);
    var lonlat = new OpenLayers.LonLat(x,y);
    
    addMarkersToLayer(layer,0);
    }



function generateMarkersList(data){
    // append each marker 
    var markerslist = new Array()
    for(i=0;i<data.length;i++) {
        markerslist[i] = new OpenLayers.Marker(
                new OpenLayers.LonLat(
                   data[i].point[0], 
                   data[i].point[1]
                )
            )
    };
    return markerslist;
};

//function: take a list of marker and a layer and add the content of marker's list to layer
function addPointsToMap(markerslist,layer,fromitem) {
    if (fromitem == markerslist.length) {
         return 0
    }
    else { 
        layer.addMarker(markerslist[fromitem]) 
        addPointsToMap(markerslist,layer,fromitem+1) 
    return 1
   }
}

//function: take a list of marker and a layer and remove the content of marker's list of layer
function removePointsMap(markerslist,layer,fromitem) {
    if (fromitem == markerslist.length) {
         return 0
    }
    else {
        layer.removeMarker(markerslist[fromitem])
        removeMarkersOfLayer(markerslist,layer,fromitem+1) 
   }
   }

function hideMarker(marker_index,layer) {
    //hide a marker. For now this function remove marker 
    from layer. 
    for(i=0;i<markers_of_layer_markers.length;i++){
         if (markers_of_layer_markers[i].id = marker_index) {
               removeMarkersOfLayer([markers_of_layer_markers[i]],layer,0);
               return 0;
         }
    }
    
}
*/

/*
------------- 
 OBJECT Point
-------------
*/


// Methods and extra attributes for object Point
Maap.Point = Maap.extend(Maap.Geom, {
    init: function() {
        size = new OpenLayers.Size(this.icon.width, this.icon.height);
        offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
        icon = new OpenLayers.Icon(this.icon.url, size, offset);
        lonlat = new OpenLayers.LonLat(this.geojson.coordinates[0],this.geojson.coordinates[1]);
        marker = new OpenLayers.Marker(lonlat, icon);
        this.layer = new OpenLayers.Layer.Markers();     
        this.layer.addMarker(marker);    
    }
})


// Extends Maap.State functionality: Add Layer
//Maap.State.prototype.loadPoint = function(pointid, callback) {
//    state = this;

    //send request to server for get the layer to add 
//    $.getJSON('/maap/json/point/'+pointid+'/', 
//        function(data) {
            // Eval layer object
//            elements = data.elements                
//            Point = new Point(data.id, data);          
//           callback(Layer);
//        }
//    );
    
//    return 0;
//};



