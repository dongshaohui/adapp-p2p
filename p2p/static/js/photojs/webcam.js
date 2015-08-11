$("#webcam").webcam({
    width: 320,
    height: 240,
    mode: "callback",
    swffile: "/static/swf/jscam_canvas_only.swf",
    onTick: function() {},
    onSave: function() {},
    onCapture: function() {},
    debug: function() {},
    onLoad: function() {}
});