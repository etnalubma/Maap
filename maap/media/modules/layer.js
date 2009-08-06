/***
    This module handles layers, and other elements, evaluating from json standard model representation    
***/

/*
------------- 
 OBJECT Layer
-------------
*/
// Initialization function for object Layer
Maap.Layer = function (metadata) {
    for (m in metadata) {
        this[m] = metadata[m];
    }
    var elms = new Array();
    
    for (i=0;i< this.elements.length; i++) {
        if (this.elements[i].type == 'point') {
            elms.push(new Maap.Point(this.elements[i]))
        } else if (this.elements[i].type == 'multiline') {
            elms.push(new Maap.MultiLine(this.elements[i]))
        }
    };
    
    this.elements = elms;
   
}

// Methods and extra attributes for object Layer
Maap.Layer.prototype = {
    
    boxCenter: function() {
        b = this.box_size
        map.zoomToExtent(new OpenLayers.Bounds(b[0],b[1],b[2],b[3]),true)
    },
    
    getLayers: function() {
        out = new Array();
        for (i=0; i < this.elements.length; i++) {
            out.push(this.elements[i].layer);
        };
        return out;
    },
    
    show: function() {
        for (i=0; i< this.elements.length; i++) {
            this.elements[i].show();
        };
        this.boxCenter();
    },
    
    hide: function() {
        for (i=0; i< this.elements.length; i++) {
            this.elements[i].hide();
        }
    },
}


// Extends Maap.State functionality: Add Layer
Maap.State.prototype.loadLayer = function(url, reload, callback) {
    state = this;

    //send request to server for get the layer to add 
    $.getJSON(url, 
        function(data) {
            // Eval layer object
            Layer = new Maap.Layer(data);          
            state.map.addLayers(Layer.getLayers());
            state.layers[Layer.id] = Layer;
            callback(Layer);
        }
    );
    return 0;
};

