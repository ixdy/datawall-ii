function Character() {
  riot.observable(this);
  
  this.arr = [];
  for (var y = 0; y < 7; y++) {
    this.arr[y] = [];
    for (var x = 0; x < 5; x++) {
      this.arr[y][x] = false;
    }
  }
  
  this.set = function (x, y, pxl) {
    this.arr[y][x] = !!pxl;
    this.trigger('changed');
  };
  
  this.get = function (x, y) {
    return this.arr[y][x];
  };
  
  this.toBytes = function() {
    var out = []
    for (var y = 0; y < 7; y++) {
      var p = 0x20;
      for (var x = 0; x < 5; x++) {
        p |= this.arr[y][x] << x;
      }
      out[y] = p;
    }
    return out;
  }
  
  this.toByteString = function(c) {
    var a = this.toBytes();
    var s = "\\x01\\x30\\xFFL\\x" + c.toString(16);
    for (var i = 0; i < 7; i++)
      s += "\\x"+a[i].toString(16);
    s += "\\x03";
    return s;
  }
}
