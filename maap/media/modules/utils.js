//this function create a position. Take a lon and lat data and do. 
function create_position(x,y) {
   var lonlat = new OpenLayers.LonLat(x,y).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
   return lonlat
}

//this function includes all necessary js files for the application  
function include(file) { 
    var script  = document.createElement('script');  
    script.src  = file;  
    script.type = 'text/javascript';  
    script.defer = true;  
    document.getElementsByTagName('head').item(0).appendChild(script);  
}

