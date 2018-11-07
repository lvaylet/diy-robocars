'use strict';

var SerialPort = require('serialport');
var portName = process.env.SERIAL || '/dev/ttyAMA0';
console.log(`Connecting to ${portName}`);
var port = new SerialPort(portName, {
  baudRate: 57600
});

port.on('open', function() {
  console.log(`Connected to ${portName}`);
});

port.on('data', function(data) {
  console.log('Received: \t', data.toString());
});
