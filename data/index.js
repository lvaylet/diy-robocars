const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const {
  exec
} = require('child_process');

server.listen(8080);

const sendSteeringValue = (socket) => {
  socket.emit('steering', {
    pulse_width_microseconds: 1500
  })
};

const sendThrottleValue = (socket) => {
  socket.emit('throttle', {
    pulse_width_microseconds: 1800
  })
};

io.on('connection', function(socket) {
  'use strict';

  console.log('a user connected');

  // Send steering and throttle values every second
  let dataLoop = setInterval(function() {
    sendSteeringValue(socket);
    sendThrottleValue(socket);
  }, 1000);

	socket.on('disconnect', function() {
      console.log('a user disconnected');
			clearInterval(dataLoop);
   });
});
