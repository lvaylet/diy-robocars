'use strict';

var SerialPort = require('serialport');
const SERIAL_PORT = process.env.SERIAL_PORT || '/dev/ttyAMA0';
const SERIAL_SPEED_BAUDS = parseInt(process.env.SERIAL_SPEED_BAUDS) || 57600;

console.log(`Connecting to ${SERIAL_PORT}...`);
var port = new SerialPort(SERIAL_PORT, {
  baudRate: SERIAL_SPEED_BAUDS
});

port.on('open', function() {
  console.log(`Connected to ${SERIAL_PORT}`);
});

port.on('data', function(data) {
  console.log('Received: ', data.toString());
});
