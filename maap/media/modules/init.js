/*** 
    This module extends the state layer to set specific initialization functions to state 
***/

//this funcion hide what layers must be available in the switcher-layers control map when the map is shown
Maap.State.prototype.initializeBaseLayers = function() {
    //layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
    layerMapnik = new OpenLayers.Layer.OSM.Mapnik("OpenStreetMap (Mapnik)",{layers: 'basic'});
    this.map.addLayer(layerMapnik); 
    this.base_layers = this.base_layers.concat(layerMapnik);
    //add here the layer that you want see in the switcher-layers control map when the map is shown. 
    
    return 0;
}

//this funcion set the initial bounds for map
Maap.State.prototype.initializeBounds = function() {
    //change this values for change de level zoom
    this.map.zoomToExtent(
        new OpenLayers.Bounds(
            -7160964.775099885,
            -3693704.7356770867,
            -7130772.148932681,
            -3678417.3300227895
        ),
        true
    );
    return 0;
}

//this function initialize the control objects of state 
Maap.State.prototype.initializeControls = function () {
    //add and/or remove controls to map
    this.map.addControl( new OpenLayers.Control.LayerSwitcher() );
    this.map.addControl( new OpenLayers.Control.MousePosition() );
    this.map.addControl( new OpenLayers.Control.PanZoomBar() );
    this.map.addControl( new OpenLayers.Control.Navigation() ); 
    this.map.addControl( new OpenLayers.Control.Attribution() );
    return 0;
}


//this function initialize all settings of state. 
Maap.State.prototype.init = function() {
    //Position: Cordoba
    var lon = -31.416667
    var lat = -64.183333
    
    //create a position indicating Cordoba
    cordoba = create_position(lon,lat);

    //add initial layers to map
    this.initializeBaseLayers();

    //center the map in Cordoba position
    map.setCenter(cordoba, 19);

    //load controls to map
    this.initializeBounds(); 

    //set the level to the user can see the map. (zoom)        
    this.initializeControls();

    return 0;

}
        

