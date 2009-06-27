/***
    This module handles layers, and other elements, evaluating from json standard model representation    
***/

/*
------------- 
 OBJECT Layer
-------------
*/
// Initialization function for object Layer
Maap.Layer = function (id, metadata) {    
    this.id = id;
    this.metadata = metadata;
    
    this.elements = new Array();
    elm = this.metadata.elements;
    
    for (i=0;i< elm.length; i++) {
        if (elm[i].type == 'point') {
            id = 'point-'+elm[i].id;
            this.elements[i] = new Maap.Point(id, elm[i])
        }
    }
    if (self.elements.length > 0) {
        this.createMarkersLayer()
    }
}

// Methods and extra attributes for object Layer
Maap.Layer.prototype = {
    base_layers: [],
    
    createMarkersLayer: function() {
        markersLayer = new OpenLayers.Layer.Markers()
        for (i=0;i<this.elements.length; i++) {
            markersLayer.addMarker(this.elements[i].marker);
        }
        // append markers layer to base_layers
        this.base_layers = this.base_layers.concat(markersLayer);
    },
    
    boxCenter: function() {
        b = this.metadata.box_size
        map.zoomToExtent(new OpenLayers.Bounds(b[0],b[1],b[2],b[3]),true)
    },
    
    getLayers: function() {
        return this.base_layers;
    },
    
    show: function() {
        for (var layer in this.base_layers) {
            this.base_layers[layer].setVisibility(true)
            this.boxCenter()
        }
    },
    
    hide: function() {
        for (var layer in this.base_layers) {
            this.base_layers[layer].setVisibility(false)
        }
    },
    addPoint: function(point) {
        this.elements[this.elements.length] = point;
        if (self.elements.length == 1) {
            this.createMarkersLayer()
        }
    }
}


// Extends Maap.State functionality: Add Layer
Maap.State.prototype.loadLayer = function(layerid, reload, callback) {
    if (reload || !(layerid in this.layers)) {
        state = this;

        //send request to server for get the layer to add 
        $.getJSON('layer/'+layerid+'/', 
            function(data) {
                // Eval layer object
                elements = data.elements                
                Layer = new Maap.Layer(data.id, data);          
                state.map.addLayers(Layer.getLayers());
                state.layers[Layer.id] = Layer;
                callback(Layer);
            }
        );
    } else if (layerid in this.layers) {
        callback(this.layers[layerid]);
    }
    
    return 0;
};

