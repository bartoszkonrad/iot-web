window.onload = load;

var ws;
var startColorChange = performance.now();
var endColorChange;

if ("WebSocket" in window) {
  // alert("WebSocket is supported by your Browser!");

  ws = new WebSocket("ws://kolasz.xyz:10080");

  ws.onopen = function() {
    var msg = {
      type: "msq",
      val: "Connection from rgb",
      date: Date.now()
    };
    if (ws) {
      ws.send(JSON.stringify(msg));
    }
    //  alert("Message is sent...");
    console.log('connected to ws server')
  };

  ws.onmessage = function (evt) {
     var received_msg = evt.data;
     alert(received_msg);
    //  alert("Message is received...");
  };

  ws.onclose = function() {
    //  alert("Connection is closed...");
  };
}
else {
  alert("WebSocket NOT supported by your Browser!");
}

function load() {
 ColorPicker(document.getElementById('color-picker'), function(hex, hsv, rgb) {
  //  console.log(hsv.h.toFixed(2), hsv.s.toFixed(2), hsv.v.toFixed(2));
  //  console.log(rgb.r, rgb.g, rgb.b); // [0-255], [0-255], [0-255]
   document.body.style.backgroundColor = hex; // #HEX
   if (document.getElementById('bdr').checked) {
     var msg = {
       type: "rgbStrip",
       h: hsv.h.toFixed(0),
       s: hsv.s.toFixed(2),
       v: hsv.v.toFixed(2),
       loc: 'bdr',
       date: Date.now()
     };
   } else if (document.getElementById('lvr').checked) {
     var msg = {
       type: "rgbStrip",
       h: hsv.h.toFixed(0),
       s: hsv.s.toFixed(2),
       v: hsv.v.toFixed(2),
       loc: 'lvr',
       date: Date.now()
     };
   }
   if (ws) {
    endColorChange = performance.now();
    if (endColorChange - startColorChange > 64) {
      ws.send(JSON.stringify(msg));
      startColorChange = performance.now();
    }
   }
 });
}

function offLedStrip() {
  console.log('off...');
  if (document.getElementById('bdr').checked) {
    var msg = {
      type: "rgbStrip",
      h: 0,
      s: 0,
      v: 0,
      loc: 'bdr',
      date: Date.now()
    };
  } else if (document.getElementById('lvr').checked) {
    var msg = {
      type: "rgbStrip",
      h: 0,
      s: 0,
      v: 0,
      loc: 'lvr',
      date: Date.now()
    };
  }
  if (ws) {
    ws.send(JSON.stringify(msg));
  }
}

function rgbPower(val) {
  console.log('off...');
  var msg = {
    type: "rgbPower",
    val: val,
    date: Date.now()
  };
  if (ws) {
    ws.send(JSON.stringify(msg));
  }
}
