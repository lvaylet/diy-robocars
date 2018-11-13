const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);

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

// --- RabbitMQ ---

// var q = 'pulse_width_microseconds';
//
// function bail(err) {
//   console.error(err);
//   process.exit(1);
// }
//
// // Publisher
// function publisher(conn) {
//   conn.createChannel(on_open);
//   function on_open(err, ch) {
//     if (err != null) bail(err);
//     ch.assertQueue(q);
//     ch.sendToQueue(q, new Buffer('something to do'));
//   }
// }
//
// // Consumer
// function consumer(conn) {
//   var ok = conn.createChannel(on_open);
//   function on_open(err, ch) {
//     if (err != null) bail(err);
//     ch.assertQueue(q);
//     ch.consume(q, function(msg) {
//       if (msg !== null) {
//         console.log(msg.content.toString());
//         ch.ack(msg);
//       }
//     });
//   }
// }
//
// require('amqplib/callback_api')
//   .connect('amqp://localhost', function(err, conn) {
//     if (err != null) bail(err);
//     consumer(conn);
//     publisher(conn);
//   });

var amqp = require('amqplib/callback_api');

amqp.connect('amqp://guest:guest@rabbitmq', function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'pulse_width_microseconds';

    ch.assertQueue(q, { durable: false });

    console.log("Waiting for messages in %s. To exit press CTRL+C", q);
    ch.consume(q, function(msg) {
      console.log("Received %s", msg.content.toString());
    }, { noAck: true });
  });
});
