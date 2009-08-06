var Maap = {}


Maap.extend = function (Parent, extra) {
    var p = Parent.prototype;
    var out = function(){
        Parent.apply(this, arguments);
    };
    for (var i in p) {
        out.prototype[i] = p[i];
    }
    out.prototype.uber = p;
    for (e in extra) {
        out.prototype[e] = extra[e];
    };
    return out;
}


/*
------------- 
 OBJECT Geom
-------------
*/
Maap.Geom = function(metadata) {
    for (m in metadata) {
        this[m] = metadata[m]
    }
    this.init();
}

Maap.Geom.prototype = {
    layer: null,
    init: function() { alert(this.id)},
    show: function() {
        this.layer.setVisibility(true);
    },
    hide: function() {
        this.layer.setVisibility(false);
    },
}





