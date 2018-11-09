const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const {
  exec
} = require('child_process');

server.listen(8080);

const getRandomArbitrary = (min, max) => {
  return Math.random() * (max - min) + min;
}

var steering_pulse_width_microseconds = 1500;
var throttle_pulse_width_microseconds = 1500;

const sendSteeringValue = (socket) => {
  steering_pulse_width_microseconds += getRandomArbitrary(-10, 10) 
  socket.emit('steering', {
    pulse_width_microseconds: steering_pulse_width_microseconds 
  })
};

const sendThrottleValue = (socket) => {
  throttle_pulse_width_microseconds += getRandomArbitrary(-10, 10)
  socket.emit('throttle', {
    pulse_width_microseconds: throttle_pulse_width_microseconds
  })
};

io.on('connection', function(socket) {
  'use strict';

  console.log('a user connected');

  // Send steering and throttle values every 200 ms
  let dataLoop = setInterval(function() {
    sendSteeringValue(socket);
    sendThrottleValue(socket);
  }, 200);

	socket.on('disconnect', function() {
      console.log('a user disconnected');
			clearInterval(dataLoop);
   });
});
