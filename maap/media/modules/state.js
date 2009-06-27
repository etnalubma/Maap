/** This module hide state of system in client and hide the implementatios of certain funcions to manipulate this state **/

/**  State Object

structure: 
        base_layers: point to list of OpenLayers layer
        layers: hold the current Maap.Layers in the map
        map: point to map
        map_options: Base options for map
**/

// Initialization function
Maap.State = function() {
    // create map whith map options     
    map = new OpenLayers.Map('map', this.map_options);

    // update the state variable
    this.map = map
};

Maap.State.prototype = {
    map: null,
    base_layers: [],
    layers: [],    
    map_options: map_options = {
           'projection' : new OpenLayers.Projection("EPSG:900913"),
           'maxResolution' : 200000.0002,
           'displayProjection' : new OpenLayers.Projection("EPSG:4326"),
           'units' : "m"
    },
    

} 






