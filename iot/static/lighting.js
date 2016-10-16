var ws;
if ("WebSocket" in window) {
  // alert("WebSocket is supported by your Browser!");

  ws = new WebSocket("ws://kolasz.xyz:10080");

  ws.onopen = function() {
    //  ws.send("Message to send");
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

function kitchenLeds(val) {
  var msg = {
    type: "kitchenLeds",
    val: val,
    date: Date.now()
  };
  if (ws) {
    ws.send(JSON.stringify(msg));
  }
}

function bathroomLeds(val) {
  var msg = {
    type: "bathroomLeds",
    val: val,
    date: Date.now()
  };
  if (ws) {
    ws.send(JSON.stringify(msg));
  }
}

function bedRoomLamps(lamp, val) {
  var msg = {
    type: "bedRoomLamps",
    lamp: lamp,
    val: val,
    date: Date.now()
  };
  if (ws) {
    ws.send(JSON.stringify(msg));
  }
}

function livingRoomLamps(lamp, val) {
  var msg = {
    type: "livingRoomLamps",
    lamp: lamp,
    val: val,
    date: Date.now()
  };
  if (ws) {
    ws.send(JSON.stringify(msg));
  }
}
