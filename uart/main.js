// This example shows the use of UART0 with a loopback. To run this correctly, you
// need to add a jumper wire between GPIO14 and GPIO15 on the RPI3.

'use strict';

var SerialPort = require('serialport');
var portName = process.env.SERIAL || '/dev/ttyAMA0';
console.log(`Connecting to ${portName}`);
var port = new SerialPort(portName);

port.on('open', function() {
  console.log(`Connected to ${portName}`);
});

port.on('data', function(data) {
  console.log('Received: \t', data.toString());
});
